import numpy as np
import cv2
from abc import ABC, abstractmethod
from picamera2 import Picamera2
import matplotlib.pyplot as plt

class CameraInterface(ABC):
    """Interface to define camera operations."""
    @abstractmethod
    def capture_image_as_array(self) -> np.ndarray:
        """Capture an image and return it as a numpy array."""
        pass

    @abstractmethod
    def get_video_frames(self):
        """Generate a stream of video frames."""
        pass

class CameraSingletonFactory:
    """Singleton factory to ensure only one camera instance is created, with configurable settings."""
    _camera_instance = None

    @staticmethod
    def get_camera(video_format: str = "RGB888", resolution: tuple = (640, 480)) -> 'Picamera2Adapter':
        """Returns the singleton camera instance with configurable settings."""
        if CameraSingletonFactory._camera_instance is None:
            CameraSingletonFactory._camera_instance = Picamera2Adapter(video_format, resolution)
        return CameraSingletonFactory._camera_instance

class Picamera2Adapter(CameraInterface):
    """Adapter for the Picamera2 library."""
    def __init__(self, video_format: str, resolution: tuple):
        self.camera = Picamera2()
        self.video_format = video_format
        self.resolution = resolution
        self.is_camera_running = False

    def start_camera(self):
        """Start the camera with custom video configuration."""
        if not self.is_camera_running:
            self.camera_config = self.camera.create_video_configuration(main={"format": self.video_format})
            self.camera.configure(self.camera_config)
            self.camera.start()
            self.is_camera_running = True

    def stop_camera(self):
        """Stop the camera if it is running."""
        if self.is_camera_running:
            self.camera.stop()
            self.is_camera_running = False

    def capture_image_as_array(self) -> np.ndarray:
        """Capture an image as a numpy array, ensuring camera is properly configured and stopped."""
        self.stop_camera()  # Ensure camera is stopped before reconfiguring
        self.camera_config = self.camera.create_still_configuration()
        self.camera.configure(self.camera_config)
        self.camera.start()
        image_array = self.camera.capture_array()
        self.camera.stop()
        self.is_camera_running = False
        return image_array

    def get_video_frames(self):
        """Yield frames from the video stream, managing camera state appropriately."""
        self.start_camera()
        try:
            while True:
                yield self.camera.capture_array()
        finally:
            self.stop_camera()

class ImageProcessor:
    """Class for processing images."""
    @staticmethod
    def save_image(image_array: np.ndarray, filename: str = "image.jpg"):
        """Save an image array to a file."""
        cv2.imwrite(filename, cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR))

    @staticmethod
    def display_image(image_array: np.ndarray):
        """Display an image array using matplotlib."""
        plt.imshow(image_array)
        plt.show()

class VideoProcessor:
    """Class for processing video streams."""
    @staticmethod
    def save_video(video_generator, filename: str = "video.mp4", num_frames: int = 100):
        """Save a certain number of video frames to a video file."""
        out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (640, 480))
        count = 0
        for frame in video_generator:
            if num_frames is not None and count >= num_frames:
                break
            out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            count += 1
        out.release()

    @staticmethod
    def display_video(video_generator, num_frames: int = None):
        """Display video frames on screen, indefinitely if num_frames is None."""
        count = 0
        for frame in video_generator:
            if num_frames is not None and count >= num_frames:
                break
            cv2.imshow('Video', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            count += 1
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Retrieve camera with custom configuration
    camera = CameraSingletonFactory.get_camera("RGB888", (640, 480))
    try:
        image_array = camera.capture_image_as_array()
        ImageProcessor.save_image(image_array, "configured_image.jpg")
        ImageProcessor.display_image(image_array)
    
        video_frames = camera.get_video_frames()
        # Example to display video, should ideally be handled with proper control flow
        for frame in video_frames:
            VideoProcessor.display_video(video_frames, 1)  # Display one frame at a time
            break  # Only display one frame for example purposes
    finally:
        camera.stop_camera()  # Ensure the camera is stopped