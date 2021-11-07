import io
import time
import struct
import binascii

from XstreamDL_CLI.models.segment import Segment


u8 = struct.Struct('>B')
u88 = struct.Struct('>Bx')
u16 = struct.Struct('>H')
u1616 = struct.Struct('>Hxx')
u32 = struct.Struct('>I')
u64 = struct.Struct('>Q')

s88 = struct.Struct('>bx')
s16 = struct.Struct('>h')
s1616 = struct.Struct('>hxx')
s32 = struct.Struct('>i')
unity_matrix = (s32.pack(0x10000) + s32.pack(0) * 3) * 2 + s32.pack(0x40000000)

TRACK_ENABLED = 0x1
TRACK_IN_MOVIE = 0x2
TRACK_IN_PREVIEW = 0x4

SELF_CONTAINED = 0x1

NALUTYPE_SPS = 7
NALUTYPE_PPS = 8


def box(box_type, payload):
    return u32.pack(8 + len(payload)) + box_type + payload


def full_box(box_type, version, flags, payload):
    return box(box_type, u8.pack(version) + u32.pack(flags)[1:] + payload)


def extract_box_data(data: bytes, box_sequence: list):
    data_reader = io.BytesIO(data)
    while True:
        box_size = u32.unpack(data_reader.read(4))[0]
        box_type = data_reader.read(4)
        if box_type == box_sequence[0]:
            box_data = data_reader.read(box_size - 8)
            if len(box_sequence) == 1:
                return box_data
            return extract_box_data(box_data, box_sequence[1:])
        data_reader.seek(box_size - 8, 1)


class MSSSegment(Segment):
    def __init__(self):
        super(MSSSegment, self).__init__()
        self.suffix = '.mp4'
        self.has_protection = True

    def set_protection_flag(self, flag: bool):
        self.has_protection = flag

    def is_encrypt(self):
        return self.has_protection

    def is_supported_encryption(self):
        return False

    def is_ism(self):
        return True

    def set_duration(self, duration: float):
        self.duration = duration

    def set_subtitle_url(self, subtitle_url: str):
        self.name = subtitle_url.split('?')[0].split('/')[-1]
        self.index = -1
        self.url = subtitle_url
        self.segment_type = 'init'

    def set_init_url(self, init_url: str):
        parts = init_url.split('?')[0].split('/')[-1].split('.')
        if len(parts) > 1:
            self.suffix = f'.{parts[-1]}'
        self.name = f'init{self.suffix}'
        self.index = -1
        self.url = init_url
        self.segment_type = 'init'

    def set_media_url(self, media_url: str):
        parts = media_url.split('?')[0].split('/')[-1].split('.')
        if len(parts) > 1:
            # 修正后缀
            self.suffix = f'.{parts[-1]}'
            self.name = f'{self.index:0>4}.{parts[-1]}'
        self.url = media_url

    def fix_header(self, stream):
        params = stream.get_ism_params()
        tfhd_data = extract_box_data(self.content[0], [b'moof', b'traf', b'tfhd'])
        track_id = u32.unpack(tfhd_data[4:8])[0]
        params['track_id'] = track_id
        self.write_piff_header(track_id, params)
        # self.write_iso6_header(track_id, params)

    @staticmethod
    def fix_header_test():
        params = {'fourcc': 'AACL', 'duration': 2537.609, 'timescale': 10000000, 'bandwidth': 64000, 'language': 'und', 'stream_type': 'audio', 'channels': 2, 'bits_per_sample': 16, 'sampling_rate': 16, 'codec_private_data': '1190', 'nal_unit_length_field': 4, 'track_id': 2}
        # track_id dashif 是根据streamindex计算的 track_id = streamindex + 1
        params['track_id'] = 2
        MSSSegment.write_iso6_header(params)

    # @staticmethod
    # def fix_header_test():
    #     params = {'fourcc': 'H264', 'duration': 2537.609, 'timescale': 10000000, 'bandwidth': 160000, 'language': 'und', 'height': 288, 'width': 512, 'stream_type': 'video', 'channels': 2, 'bits_per_sample': 16, 'sampling_rate': 16, 'codec_private_data': '000000016742C01ED9008025B0110000030001000003003C0F162E480000000168CB8CB2', 'nal_unit_length_field': 4, 'track_id': 2}
    #    # track_id dashif 是根据streamindex计算的 track_id = streamindex + 1
    #     params['track_id'] = 1
    #     MSSSegment.write_iso6_header(params)

    @staticmethod
    def write_iso6_header(params: dict, write_time: bool = False):
        def get_sinf_payload(codec: bytes):
            sinf_payload = box(b'frma', codec)

            schm_payload = u32.pack(0x63656E63) # scheme_type 'cenc' => common encryption
            schm_payload += u32.pack(0x00010000) # scheme_version Major version 1, Minor version 0
            sinf_payload += full_box(b'schm', 0, 0, schm_payload)

            tenc_payload = u8.pack(0x0) * 2
            tenc_payload += u8.pack(0x1) # default_IsEncrypted
            tenc_payload += u8.pack(0x8) # default_IV_size
            tenc_payload += kid # default_KID
            tenc_payload = full_box(b'tenc', 0, 0, tenc_payload)
            sinf_payload += box(b'schi', tenc_payload)
            sinf_payload = box(b'sinf', sinf_payload)
            return sinf_payload
        print(params)
        # track info
        representation_id = 'audio_0'
        # representation_id = 'video_7'
        track_id = params['track_id']
        fourcc = params['fourcc']
        duration = params['duration']
        timescale = params.get('timescale', 10000000)
        language = params.get('language', 'und')
        height = params.get('height', 0)
        width = params.get('width', 0)
        bandwidth = params.get('bandwidth', 0)
        kid = params.get('kid', bytes([0] * 16))
        stream_type = params['stream_type']
        kid = bytes.fromhex('b6e16839eebd4ff6ab768d482d8d2b6a') # default_KID
        if write_time:
            creation_time = modification_time = int(time.time())
        else:
            creation_time = modification_time = 0

        # ftyp box
        ftyp_payload = b'iso6' # major brand
        ftyp_payload += u32.pack(1) # minor version
        ftyp_payload += b'isom' + b'iso6' + b'msdh' # compatible brands

        mvhd_payload = u64.pack(creation_time)
        mvhd_payload += u64.pack(modification_time)
        mvhd_payload += u32.pack(timescale)
        mvhd_payload += u64.pack(int(duration * timescale))
        mvhd_payload += s1616.pack(1) # rate
        mvhd_payload += s88.pack(1) # volume
        mvhd_payload += u16.pack(0) # reserved1
        mvhd_payload += u32.pack(0) * 2 # reserved2
        mvhd_payload += unity_matrix
        mvhd_payload += u32.pack(0) * 6 # pre defined
        # 需要确认是不是要 +1
        mvhd_payload += u32.pack(track_id + 1) # next track id
        moov_payload = full_box(b'mvhd', 1, 0, mvhd_payload) # Movie Header Box

        tkhd_payload = u64.pack(creation_time)
        tkhd_payload += u64.pack(modification_time)
        tkhd_payload += u32.pack(track_id) # track id
        tkhd_payload += u32.pack(0) # reserved1
        tkhd_payload += u64.pack(int(duration * timescale))
        tkhd_payload += u32.pack(0) * 2 # reserved2
        tkhd_payload += s16.pack(0) # layer
        tkhd_payload += s16.pack(0) # alternate group
        # 1.0 ???
        tkhd_payload += s88.pack(1) # volume
        tkhd_payload += u16.pack(0) # reserved3
        tkhd_payload += unity_matrix
        tkhd_payload += u1616.pack(width)
        tkhd_payload += u1616.pack(height)
        trak_payload = full_box(b'tkhd', 1, TRACK_ENABLED | TRACK_IN_MOVIE | TRACK_IN_PREVIEW, tkhd_payload) # Track Header Box

        mdhd_payload = u64.pack(creation_time)
        mdhd_payload += u64.pack(modification_time)
        mdhd_payload += u32.pack(timescale)
        mdhd_payload += u64.pack(int(duration * timescale))
        mdhd_payload += u16.pack(((ord(language[0]) - 0x60) << 10) | ((ord(language[1]) - 0x60) << 5) | (ord(language[2]) - 0x60))
        mdhd_payload += u16.pack(0) # pre defined
        mdia_payload = full_box(b'mdhd', 1, 0, mdhd_payload) # Media Header Box

        hdlr_payload = u32.pack(0) # pre defined
        if stream_type == 'video': # handler type
            hdlr_payload += b'vide'
        elif stream_type == 'audio':
            hdlr_payload += b'soun'
        elif stream_type == 'text':
            hdlr_payload += b'subt'
        else:
            hdlr_payload += b'meta'
            assert False
        hdlr_payload += u32.pack(0) * 3 # reserved
        hdlr_payload += representation_id.encode('utf-8') + b'\0' # name
        mdia_payload += full_box(b'hdlr', 0, 0, hdlr_payload) # Handler Reference Box

        if stream_type == 'video':
            vmhd_payload = u16.pack(0) # graphics mode
            vmhd_payload += u16.pack(0) * 3 # opcolor
            media_header_box = full_box(b'vmhd', 0, 1, vmhd_payload) # Video Media Header
        elif stream_type == 'audio':
            smhd_payload = s88.pack(0) # balance
            smhd_payload += u16.pack(0) # reserved
            media_header_box = full_box(b'smhd', 0, 1, smhd_payload) # Sound Media Header
        elif stream_type == 'text':
            media_header_box = full_box(b'sthd', 0, 1, b'') # Subtitle Media Header
        else:
            assert False
        minf_payload = media_header_box

        dref_payload = u32.pack(1) # entry count
        dref_payload += full_box(b'url ', 0, SELF_CONTAINED, b'') # Data Entry URL Box
        dinf_payload = full_box(b'dref', 0, 0, dref_payload) # Data Reference Box
        minf_payload += box(b'dinf', dinf_payload) # Data Information Box

        stsd_payload = u32.pack(1) # entry count

        sample_entry_payload = u8.pack(0) * 6 # reserved
        sample_entry_payload += u16.pack(1) # data reference index
        if stream_type == 'audio':
            sample_entry_payload += u32.pack(0) * 2 # reserved2
            sample_entry_payload += u16.pack(params.get('channels', 2))
            sample_entry_payload += u16.pack(params.get('bits_per_sample', 16))
            sample_entry_payload += u16.pack(0) # pre defined
            sample_entry_payload += u16.pack(0) # reserved3
            # 注意检查
            sample_entry_payload += u1616.pack(params['sampling_rate'])
            if fourcc == 'AACL':
                sample_entry_box = box(b'mp4a', sample_entry_payload)

            audioSpecificConfig = bytes.fromhex(params['codec_private_data'])

            # ESDS length = esds box header length (= 12) +
            #               ES_Descriptor header length (= 5) +
            #               DecoderConfigDescriptor header length (= 15) +
            #               decoderSpecificInfo header length (= 2) +
            #               AudioSpecificConfig length (= codecPrivateData length)
            # esdsLength = 34 + len(audioSpecificConfig)

            # ES_Descriptor (see ISO/IEC 14496-1 (Systems))
            esds_payload = u8.pack(0x03) # tag = 0x03 (ES_DescrTag)
            esds_payload += u8.pack(20 + len(audioSpecificConfig)) # size
            esds_payload += u8.pack((track_id & 0xFF00) >> 8) # ES_ID = track_id
            esds_payload += u8.pack(track_id & 0x00FF)
            esds_payload += u8.pack(0) # flags and streamPriority

            # DecoderConfigDescriptor (see ISO/IEC 14496-1 (Systems))
            esds_payload += u8.pack(0x04) # tag = 0x04 (DecoderConfigDescrTag)
            esds_payload += u8.pack(15 + len(audioSpecificConfig)) # size
            esds_payload += u8.pack(0x40) # objectTypeIndication = 0x40 (MPEG-4 AAC)
            # esds_payload[i] = 0x05 << 2 # streamType = 0x05 (Audiostream)
            # esds_payload[i] |= 0 << 1 # upStream = 0
            esds_payload += u8.pack((0x05 << 2) | (0 << 1) | 1) # reserved = 1
            esds_payload += u8.pack(0xFF) # buffersizeDB = undefined
            esds_payload += u8.pack(0xFF) # ''
            esds_payload += u8.pack(0xFF) # ''
            esds_payload += u8.pack((bandwidth & 0xFF000000) >> 24) # maxBitrate
            esds_payload += u8.pack((bandwidth & 0x00FF0000) >> 16) # ''
            esds_payload += u8.pack((bandwidth & 0x0000FF00) >> 8) # ''
            esds_payload += u8.pack((bandwidth & 0x000000FF)) # ''
            esds_payload += u8.pack((bandwidth & 0xFF000000) >> 24) # avgbitrate
            esds_payload += u8.pack((bandwidth & 0x00FF0000) >> 16) # ''
            esds_payload += u8.pack((bandwidth & 0x0000FF00) >> 8) # ''
            esds_payload += u8.pack((bandwidth & 0x000000FF)) # ''

            # DecoderSpecificInfo (see ISO/IEC 14496-1 (Systems))
            esds_payload += u8.pack(0x05) # tag = 0x05 (DecSpecificInfoTag)
            esds_payload += u8.pack(len(audioSpecificConfig)) # size
            esds_payload += audioSpecificConfig # AudioSpecificConfig bytes

            sample_entry_payload += full_box(b'esds', 0, 0, esds_payload) + get_sinf_payload(b'mp4a') # AVC Decoder Configuration Record
            sample_entry_box = box(b'enca', sample_entry_payload) # AVC Simple Entry
        elif stream_type == 'video':
            sample_entry_payload += u16.pack(0) # pre defined
            sample_entry_payload += u16.pack(0) # reserved
            sample_entry_payload += u32.pack(0) * 3 # pre defined
            sample_entry_payload += u16.pack(width)
            sample_entry_payload += u16.pack(height)
            sample_entry_payload += u1616.pack(0x48) # horiz resolution 72 dpi
            sample_entry_payload += u1616.pack(0x48) # vert resolution 72 dpi
            sample_entry_payload += u32.pack(0) # reserved
            sample_entry_payload += u16.pack(1) # frame count
            # sample_entry_payload += u8.pack(0) * 32 # compressor name
            sample_entry_payload += bytes([
                0x0A, 0x41, 0x56, 0x43, 0x20, 0x43, 0x6F, 0x64,
                0x69, 0x6E, 0x67, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            ]) # compressor name
            sample_entry_payload += u16.pack(0x18) # depth
            sample_entry_payload += u16.pack(65535) # pre defined3

            if fourcc in ('H264', 'AVC1'):
                # avcCLength = 15
                sps = []
                pps = []
                nalus = params['codec_private_data'].split('00000001')[1:]
                for nalu in nalus:
                    naluBytes = bytes.fromhex(nalu)
                    naluType = naluBytes[0] & 0x1F
                    if naluType == NALUTYPE_SPS:
                        sps.append(naluBytes)
                        # avcCLength += len(naluBytes) + 2 # 2 = sequenceParameterSetLength field length
                    elif naluType == NALUTYPE_PPS:
                        # avcCLength += len(naluBytes) + 2 # 2 = pictureParameterSetLength field length
                        pps.append(naluBytes)
                    else:
                        pass
                if len(sps) > 0:
                    AVCProfileIndication = sps[0][1]
                    profile_compatibility = sps[0][2]
                    AVCLevelIndication = sps[0][3]
                else:
                    AVCProfileIndication = 0
                    profile_compatibility = 0
                    AVCLevelIndication = 0
                # 这里不知道为什么没用上
                # avcc_head_payload = bytes([
                #     (avcCLength & 0xFF000000) >> 24,
                #     (avcCLength & 0x00FF0000) >> 16,
                #     (avcCLength & 0x0000FF00) >> 8,
                #     (avcCLength & 0x000000FF),
                # ])

                avcc_payload = u8.pack(1) # configurationVersion = 1
                avcc_payload += u8.pack(AVCProfileIndication)
                avcc_payload += u8.pack(profile_compatibility)
                avcc_payload += u8.pack(AVCLevelIndication)
                avcc_payload += u8.pack(0xFF) # '11111' + lengthSizeMinusOne = 3
                avcc_payload += u8.pack(0xE0 | len(sps)) # '111' + numOfSequenceParameterSets
                for item in sps:
                    avcc_payload += u8.pack((len(item) & 0xFF00) >> 8)
                    avcc_payload += u8.pack((len(item) & 0x00FF))
                    avcc_payload += item
                avcc_payload += u8.pack(len(pps)) # numOfPictureParameterSets
                for item in pps:
                    avcc_payload += u8.pack((len(item) & 0xFF00) >> 8)
                    avcc_payload += u8.pack((len(item) & 0x00FF))
                    avcc_payload += item

                sample_entry_payload += box(b'avcC', avcc_payload) + get_sinf_payload(b'avc1') # AVC Decoder Configuration Record
                sample_entry_box = box(b'encv', sample_entry_payload) # AVC Simple Entry
            else:
                assert False
        elif stream_type == 'text':
            if fourcc == 'TTML':
                sample_entry_payload += b'http://www.w3.org/ns/ttml\0' # namespace
                sample_entry_payload += b'\0' # schema location
                sample_entry_payload += b'\0' # auxilary mime types(??)
                sample_entry_box = box(b'stpp', sample_entry_payload)
            else:
                assert False
        else:
            assert False

        stts_payload = u32.pack(0) # entry count
        stbl_payload = full_box(b'stts', 0, 0, stts_payload) # Decoding Time to Sample Box

        stsc_payload = u32.pack(0) # entry count
        stbl_payload += full_box(b'stsc', 0, 0, stsc_payload) # Sample To Chunk Box

        stco_payload = u32.pack(0) # entry count
        stbl_payload += full_box(b'stco', 0, 0, stco_payload) # Chunk Offset Box

        stsz_payload = u32.pack(0) + u32.pack(0) # sample size, sample count
        stbl_payload += full_box(b'stsz', 0, 0, stsz_payload) # Sample Size Box

        stsd_payload += sample_entry_box
        stbl_payload += full_box(b'stsd', 0, 0, stsd_payload) # Sample Description Box

        minf_payload += box(b'stbl', stbl_payload) # Sample Table Box
        mdia_payload += box(b'minf', minf_payload) # Media Information Box
        trak_payload += box(b'mdia', mdia_payload) # Media Box
        moov_payload += box(b'trak', trak_payload) # Track Box

        trex_payload = u32.pack(track_id) # track id
        trex_payload += u32.pack(1) # default sample description index
        trex_payload += u32.pack(0) # default sample duration
        trex_payload += u32.pack(0) # default sample size
        trex_payload += u32.pack(0) # default sample flags
        mvex_payload = full_box(b'trex', 0, 0, trex_payload) # Track Extends Box
        moov_payload += box(b'mvex', mvex_payload) # Movie Extends Box
        moov_payload = box(b'moov', moov_payload)
        moov_payload = box(b'ftyp', ftyp_payload) + moov_payload
        from pathlib import Path
        Path(r'C:\Users\weimo\Downloads\tutorial muxing init\tutorial muxing init\FILES\rrr0a.bin').write_bytes(moov_payload)
        # self.content.insert(0, box(b'moov', moov_payload))

    def write_piff_header(self, track_id: int, params: dict):

        track_id = params['track_id']
        fourcc = params['fourcc']
        duration = params['duration']
        timescale = params.get('timescale', 10000000)
        language = params.get('language', 'und')
        height = params.get('height', 0)
        width = params.get('width', 0)
        stream_type = params['stream_type']
        creation_time = modification_time = int(time.time())

        ftyp_payload = b'isml' # major brand
        ftyp_payload += u32.pack(1) # minor version
        ftyp_payload += b'piff' + b'iso2' # compatible brands
        self.content.insert(0, box(b'ftyp', ftyp_payload))

        mvhd_payload = u64.pack(creation_time)
        mvhd_payload += u64.pack(modification_time)
        mvhd_payload += u32.pack(timescale)
        mvhd_payload += u64.pack(duration)
        mvhd_payload += s1616.pack(1) # rate
        mvhd_payload += s88.pack(1) # volume
        mvhd_payload += u16.pack(0) # reserved
        mvhd_payload += u32.pack(0) * 2 # reserved
        mvhd_payload += unity_matrix
        mvhd_payload += u32.pack(0) * 6 # pre defined
        mvhd_payload += u32.pack(0xffffffff) # next track id
        moov_payload = full_box(b'mvhd', 1, 0, mvhd_payload) # Movie Header Box

        tkhd_payload = u64.pack(creation_time)
        tkhd_payload += u64.pack(modification_time)
        tkhd_payload += u32.pack(track_id) # track id
        tkhd_payload += u32.pack(0) # reserved
        tkhd_payload += u64.pack(duration)
        tkhd_payload += u32.pack(0) * 2 # reserved
        tkhd_payload += s16.pack(0) # layer
        tkhd_payload += s16.pack(0) # alternate group
        tkhd_payload += s88.pack(1 if stream_type == 'audio' else 0) # volume
        tkhd_payload += u16.pack(0) # reserved
        tkhd_payload += unity_matrix
        tkhd_payload += u1616.pack(width)
        tkhd_payload += u1616.pack(height)
        trak_payload = full_box(b'tkhd', 1, TRACK_ENABLED | TRACK_IN_MOVIE | TRACK_IN_PREVIEW, tkhd_payload) # Track Header Box

        mdhd_payload = u64.pack(creation_time)
        mdhd_payload += u64.pack(modification_time)
        mdhd_payload += u32.pack(timescale)
        mdhd_payload += u64.pack(duration)
        mdhd_payload += u16.pack(((ord(language[0]) - 0x60) << 10) | ((ord(language[1]) - 0x60) << 5) | (ord(language[2]) - 0x60))
        mdhd_payload += u16.pack(0) # pre defined
        mdia_payload = full_box(b'mdhd', 1, 0, mdhd_payload) # Media Header Box

        hdlr_payload = u32.pack(0) # pre defined
        if stream_type == 'audio': # handler type
            hdlr_payload += b'soun'
            hdlr_payload += u32.pack(0) * 3 # reserved
            hdlr_payload += b'SoundHandler\0' # name
        elif stream_type == 'video':
            hdlr_payload += b'vide'
            hdlr_payload += u32.pack(0) * 3 # reserved
            hdlr_payload += b'VideoHandler\0' # name
        elif stream_type == 'text':
            hdlr_payload += b'subt'
            hdlr_payload += u32.pack(0) * 3 # reserved
            hdlr_payload += b'SubtitleHandler\0' # name
        else:
            assert False
        mdia_payload += full_box(b'hdlr', 0, 0, hdlr_payload) # Handler Reference Box

        if stream_type == 'audio':
            smhd_payload = s88.pack(0) # balance
            smhd_payload += u16.pack(0) # reserved
            media_header_box = full_box(b'smhd', 0, 0, smhd_payload) # Sound Media Header
        elif stream_type == 'video':
            vmhd_payload = u16.pack(0) # graphics mode
            vmhd_payload += u16.pack(0) * 3 # opcolor
            media_header_box = full_box(b'vmhd', 0, 1, vmhd_payload) # Video Media Header
        elif stream_type == 'text':
            media_header_box = full_box(b'sthd', 0, 0, b'') # Subtitle Media Header
        else:
            assert False
        minf_payload = media_header_box

        dref_payload = u32.pack(1) # entry count
        dref_payload += full_box(b'url ', 0, SELF_CONTAINED, b'') # Data Entry URL Box
        dinf_payload = full_box(b'dref', 0, 0, dref_payload) # Data Reference Box
        minf_payload += box(b'dinf', dinf_payload) # Data Information Box

        stsd_payload = u32.pack(1) # entry count

        sample_entry_payload = u8.pack(0) * 6 # reserved
        sample_entry_payload += u16.pack(1) # data reference index
        if stream_type == 'audio':
            sample_entry_payload += u32.pack(0) * 2 # reserved
            sample_entry_payload += u16.pack(params.get('channels', 2))
            sample_entry_payload += u16.pack(params.get('bits_per_sample', 16))
            sample_entry_payload += u16.pack(0) # pre defined
            sample_entry_payload += u16.pack(0) # reserved
            sample_entry_payload += u1616.pack(params['sampling_rate'])

            if fourcc == 'AACL':
                sample_entry_box = box(b'mp4a', sample_entry_payload)
        elif stream_type == 'video':
            sample_entry_payload += u16.pack(0) # pre defined
            sample_entry_payload += u16.pack(0) # reserved
            sample_entry_payload += u32.pack(0) * 3 # pre defined
            sample_entry_payload += u16.pack(width)
            sample_entry_payload += u16.pack(height)
            sample_entry_payload += u1616.pack(0x48) # horiz resolution 72 dpi
            sample_entry_payload += u1616.pack(0x48) # vert resolution 72 dpi
            sample_entry_payload += u32.pack(0) # reserved
            sample_entry_payload += u16.pack(1) # frame count
            sample_entry_payload += u8.pack(0) * 32 # compressor name
            sample_entry_payload += u16.pack(0x18) # depth
            sample_entry_payload += s16.pack(-1) # pre defined

            codec_private_data = binascii.unhexlify(params['codec_private_data'].encode('utf-8'))
            if fourcc in ('H264', 'AVC1'):
                sps, pps = codec_private_data.split(u32.pack(1))[1:]
                avcc_payload = u8.pack(1) # configuration version
                avcc_payload += sps[1:4] # avc profile indication + profile compatibility + avc level indication
                avcc_payload += u8.pack(0xfc | (params.get('nal_unit_length_field', 4) - 1)) # complete representation (1) + reserved (11111) + length size minus one
                avcc_payload += u8.pack(1) # reserved (0) + number of sps (0000001)
                avcc_payload += u16.pack(len(sps))
                avcc_payload += sps
                avcc_payload += u8.pack(1) # number of pps
                avcc_payload += u16.pack(len(pps))
                avcc_payload += pps
                sample_entry_payload += box(b'avcC', avcc_payload) # AVC Decoder Configuration Record
                sample_entry_box = box(b'avc1', sample_entry_payload) # AVC Simple Entry
            else:
                assert False
        elif stream_type == 'text':
            if fourcc == 'TTML':
                sample_entry_payload += b'http://www.w3.org/ns/ttml\0' # namespace
                sample_entry_payload += b'\0' # schema location
                sample_entry_payload += b'\0' # auxilary mime types(??)
                sample_entry_box = box(b'stpp', sample_entry_payload)
            else:
                assert False
        else:
            assert False
        stsd_payload += sample_entry_box

        stbl_payload = full_box(b'stsd', 0, 0, stsd_payload) # Sample Description Box

        stts_payload = u32.pack(0) # entry count
        stbl_payload += full_box(b'stts', 0, 0, stts_payload) # Decoding Time to Sample Box

        stsc_payload = u32.pack(0) # entry count
        stbl_payload += full_box(b'stsc', 0, 0, stsc_payload) # Sample To Chunk Box

        stco_payload = u32.pack(0) # entry count
        stbl_payload += full_box(b'stco', 0, 0, stco_payload) # Chunk Offset Box

        minf_payload += box(b'stbl', stbl_payload) # Sample Table Box

        mdia_payload += box(b'minf', minf_payload) # Media Information Box

        trak_payload += box(b'mdia', mdia_payload) # Media Box

        moov_payload += box(b'trak', trak_payload) # Track Box

        mehd_payload = u64.pack(duration)
        mvex_payload = full_box(b'mehd', 1, 0, mehd_payload) # Movie Extends Header Box

        trex_payload = u32.pack(track_id) # track id
        trex_payload += u32.pack(1) # default sample description index
        trex_payload += u32.pack(0) # default sample duration
        trex_payload += u32.pack(0) # default sample size
        trex_payload += u32.pack(0) # default sample flags
        mvex_payload += full_box(b'trex', 0, 0, trex_payload) # Track Extends Box

        moov_payload += box(b'mvex', mvex_payload) # Movie Extends Box

        self.content.insert(1, box(b'moov', moov_payload)) # Movie Box


if __name__ == '__main__':
    MSSSegment.fix_header_test()