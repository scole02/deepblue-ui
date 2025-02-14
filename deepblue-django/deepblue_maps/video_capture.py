import cv2
import gi
import numpy as np
import os
from datetime import datetime
from django.conf import settings

gi.require_version('Gst', '1.0')
from gi.repository import Gst






class VideoHandler():
    def __init__(self, port=5600):
        Gst.init(None)
        self.port = port
        self.latest_frame = self._new_frame = None
        self.video_source = 'udpsrc port={}'.format(self.port)
        self.video_codec = '! application/x-rtp, payload=96 ! rtph264depay ! h264parse ! avdec_h264'
        self.video_decode = '! decodebin ! videoconvert ! video/x-raw,format=(string)BGR ! videoconvert'
        self.video_sink_conf = '! appsink emit-signals=true sync=false max-buffers=2 drop=true'
        self.video_pipe = None
        self.video_sink = None
        self.video_file_path = None
        self.recording = False
        self.run()

    def start_gst(self, config=None):
        """ Start gstreamer pipeline and sink """
        if not config:
            config = [
                'videotestsrc ! decodebin',
                '! videoconvert ! video/x-raw,format=(string)BGR ! videoconvert',
                '! appsink'
            ]

        command = ' '.join(config)
        self.video_pipe = Gst.parse_launch(command)
        self.video_pipe.set_state(Gst.State.PLAYING)
        self.video_sink = self.video_pipe.get_by_name('appsink0')

    @staticmethod
    def gst_to_opencv(sample):
        """Transform byte array into np array"""
        buf = sample.get_buffer()
        caps_structure = sample.get_caps().get_structure(0)
        array = np.ndarray(
            (
                caps_structure.get_value('height'),
                caps_structure.get_value('width'),
                3
            ),
            buffer=buf.extract_dup(0, buf.get_size()), dtype=np.uint8)
        return array

    def frame(self):
        """Get Frame"""
        if self.frame_available():
            self.latest_frame = self._new_frame
            self._new_frame = None
        return self.latest_frame

    def frame_available(self):
        """Check if a new frame is available"""
        return self._new_frame is not None

    def run(self):
        """Get frame to update _new_frame"""
        self.start_gst(
            [
                self.video_source,
                self.video_codec,
                self.video_decode,
                self.video_sink_conf
            ]
        )
        self.video_sink.connect('new-sample', self.callback)

    def callback(self, sink):
        sample = sink.emit('pull-sample')
        self._new_frame = self.gst_to_opencv(sample)
        return Gst.FlowReturn.OK


    def start_recording(self, video_path):
        """Start recording video to the specified path."""
        if self.recording:
            print("Already recording!")
            return
        
        # Wait for first frame to get dimensions
        while not self.frame_available():
            cv2.waitKey(30)
        
        # use media root to save the video
        video_path = os.path.join(settings.MEDIA_ROOT, video_path)
        frame = self.frame()
        height, width = frame.shape[:2]
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(
            video_path,
            fourcc,
            30.0,  # fps
            (width, height)
        )
        self.video_file_path = video_path
        self.recording = True
        
        # Start recording thread
        def record_frames():
            while self.recording:
                if self.frame_available():
                    frame = self.frame()
                    self.video_writer.write(frame)
                cv2.waitKey(33)  # ~30fps
        
        from threading import Thread
        self.recording_thread = Thread(target=record_frames)
        self.recording_thread.start()

    def stop_recording(self):
        """Stop recording and save the video file."""
        if not self.recording:
            print("Not recording!")
            return
            
        self.recording = False
        self.recording_thread.join()  # Wait for recording thread to finish
        
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
            
        return self.video_file_path
    
    
if __name__ == '__main__':
    video_handler = VideoHandler("4777")
    video_handler.start_recording('video.mp4')
    cv2.waitKey(10000)  # Record for 10 seconds
    video_handler.stop_recording()
    print("Recording saved to video.mp4")
    cv2.destroyAllWindows()
    # os.system(f'ffplay -autoexit {video_handler.video_file_path}')