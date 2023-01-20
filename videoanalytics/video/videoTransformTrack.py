from aiortc import MediaStreamTrack
from av.frame import Frame
from av.video.frame import VideoFrame

from videoanalytics.analytics import Analyzer


class VideoTransformTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self, track, analyzer: Analyzer):
        super().__init__()
        self.track = track
        self._analyzer = analyzer

    async def recv(self) -> Frame:
        source_frame = await self.track.recv()
        frame = self._analyzer.process_frame(source_frame.to_ndarray(format="bgr24"))
        new_frame = VideoFrame.from_ndarray(frame, format="bgr24")
        new_frame.pts = source_frame.pts
        new_frame.time_base = source_frame.time_base
        return new_frame
