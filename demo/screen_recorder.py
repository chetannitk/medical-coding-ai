"""
Screen recording automation script for capturing live demo.
Works on macOS, Windows, and Linux.
"""

import subprocess
import sys
import os
import time
import platform
from pathlib import Path


class ScreenRecorder:
    """Cross-platform screen recording for demo video creation."""
    
    def __init__(self):
        self.system = platform.system()
        self.demo_dir = Path("demo")
        self.demo_dir.mkdir(exist_ok=True)
        
    def check_recording_tools(self):
        """Check available screen recording tools."""
        if self.system == "Darwin":  # macOS
            return self._check_macos_tools()
        elif self.system == "Linux":
            return self._check_linux_tools()
        elif self.system == "Windows":
            return self._check_windows_tools()
        else:
            print(f"❌ Unsupported system: {self.system}")
            return False
    
    def _check_macos_tools(self):
        """Check macOS recording tools."""
        try:
            # Check for ffmpeg (preferred)
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            print("✅ ffmpeg available for screen recording")
            return "ffmpeg"
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("📦 Installing ffmpeg via Homebrew...")
            try:
                subprocess.run(["brew", "install", "ffmpeg"], check=True)
                print("✅ ffmpeg installed successfully")
                return "ffmpeg"
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("⚠️  Homebrew not found. Using macOS built-in screen capture")
                return "macos_builtin"
    
    def _check_linux_tools(self):
        """Check Linux recording tools."""
        tools = ["ffmpeg", "recordmydesktop", "kazam"]
        for tool in tools:
            try:
                subprocess.run([tool, "--version"], capture_output=True, check=True)
                print(f"✅ {tool} available for screen recording")
                return tool
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        print("📦 Installing ffmpeg...")
        try:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "ffmpeg"], check=True)
            return "ffmpeg"
        except subprocess.CalledProcessError:
            print("❌ Could not install screen recording tools")
            return False
    
    def _check_windows_tools(self):
        """Check Windows recording tools."""
        try:
            # Check for ffmpeg
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            print("✅ ffmpeg available for screen recording")
            return "ffmpeg"
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  ffmpeg not found. Please install ffmpeg for Windows")
            print("    Download from: https://ffmpeg.org/download.html")
            return False
    
    def record_demo_automated(self, duration=60):
        """Record automated demo with terminal output."""
        tool = self.check_recording_tools()
        if not tool:
            return False
        
        print(f"🎬 Starting {duration}-second screen recording...")
        print("📱 Make sure your terminal is visible and ready")
        
        # Countdown
        for i in range(5, 0, -1):
            print(f"⏰ Recording starts in {i}...")
            time.sleep(1)
        
        output_file = self.demo_dir / "demo_recording.mp4"
        
        if tool == "ffmpeg":
            return self._record_with_ffmpeg(output_file, duration)
        elif tool == "macos_builtin":
            return self._record_macos_builtin(output_file, duration)
        else:
            print(f"❌ Recording tool {tool} not implemented")
            return False
    
    def _record_with_ffmpeg(self, output_file, duration):
        """Record using ffmpeg."""
        if self.system == "Darwin":  # macOS
            # macOS ffmpeg command
            cmd = [
                "ffmpeg", "-f", "avfoundation", "-r", "30",
                "-i", "1:0",  # Screen:Audio
                "-t", str(duration),
                "-c:v", "libx264", "-preset", "fast",
                "-c:a", "aac", "-b:a", "128k",
                str(output_file)
            ]
        elif self.system == "Linux":
            # Linux ffmpeg command
            cmd = [
                "ffmpeg", "-f", "x11grab", "-r", "30",
                "-s", "1920x1080", "-i", ":0.0",
                "-t", str(duration),
                "-c:v", "libx264", "-preset", "fast",
                str(output_file)
            ]
        else:  # Windows
            cmd = [
                "ffmpeg", "-f", "gdigrab", "-r", "30",
                "-i", "desktop",
                "-t", str(duration),
                "-c:v", "libx264", "-preset", "fast",
                str(output_file)
            ]
        
        try:
            print(f"🔴 Recording started... ({duration} seconds)")
            subprocess.run(cmd, check=True)
            print(f"✅ Recording saved to: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Recording failed: {e}")
            return False
    
    def _record_macos_builtin(self, output_file, duration):
        """Record using macOS built-in screen capture."""
        cmd = [
            "screencapture", "-v", 
            "-t", "10",  # 10 second delay
            str(output_file)
        ]
        
        try:
            print("📸 Using macOS screen capture...")
            print("⏰ Recording will start in 10 seconds")
            subprocess.run(cmd, check=True)
            print(f"✅ Recording saved to: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Recording failed: {e}")
            return False
    
    def run_demo_with_recording(self):
        """Run demo and record simultaneously."""
        print("🎬 AUTOMATED DEMO RECORDING")
        print("=" * 40)
        
        # Start recording
        recording_process = None
        
        try:
            # Check tools
            tool = self.check_recording_tools()
            if not tool:
                print("❌ No recording tools available")
                return False
            
            print("🎯 Preparing to record demo...")
            print("📋 Demo will run automatically while recording")
            
            # Countdown
            for i in range(5, 0, -1):
                print(f"⏰ Starting in {i}...")
                time.sleep(1)
            
            # Start recording in background
            output_file = self.demo_dir / "demo_with_terminal.mp4"
            
            if tool == "ffmpeg" and self.system == "Darwin":
                recording_cmd = [
                    "ffmpeg", "-f", "avfoundation", "-r", "30",
                    "-i", "1:0", "-t", "60",
                    "-c:v", "libx264", "-preset", "fast",
                    str(output_file)
                ]
                
                recording_process = subprocess.Popen(recording_cmd)
                print("🔴 Recording started...")
                
                # Wait a moment for recording to stabilize
                time.sleep(2)
                
                # Run the demo
                print("🚀 Starting demo presentation...")
                demo_cmd = [sys.executable, "demo/quick_demo.py"]
                subprocess.run(demo_cmd)
                
                # Wait for recording to finish
                recording_process.wait()
                print(f"✅ Demo recorded to: {output_file}")
                return True
            
            else:
                print("⚠️  Automated recording not available for this system")
                print("📝 Please manually record while running:")
                print("    python demo/quick_demo.py")
                return False
                
        except KeyboardInterrupt:
            print("\n🛑 Recording interrupted by user")
            if recording_process:
                recording_process.terminate()
            return False
        except Exception as e:
            print(f"❌ Recording error: {e}")
            if recording_process:
                recording_process.terminate()
            return False


def create_gif_from_recording():
    """Convert MP4 to GIF for easy sharing."""
    try:
        import subprocess
        
        input_file = "demo/demo_recording.mp4"
        output_file = "demo/demo_preview.gif"
        
        if not os.path.exists(input_file):
            print("❌ No recording found to convert")
            return False
        
        # Convert to GIF using ffmpeg
        cmd = [
            "ffmpeg", "-i", input_file,
            "-vf", "fps=10,scale=800:-1:flags=lanczos",
            "-t", "30",  # First 30 seconds
            output_file
        ]
        
        subprocess.run(cmd, check=True)
        print(f"✅ GIF preview created: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ GIF conversion failed: {e}")
        return False


def main():
    """Main recording interface."""
    recorder = ScreenRecorder()
    
    print("🎬 MEDICAL CODING AI - VIDEO RECORDER")
    print("=" * 45)
    print()
    print("Choose recording option:")
    print("1. Record live demo (60 seconds)")
    print("2. Create slideshow video")
    print("3. Automated demo + recording")
    print("4. Create GIF preview")
    print()
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🎥 Manual Recording Mode")
        print("1. Start your screen recorder")
        print("2. Run: python demo/quick_demo.py")
        print("3. Stop recording when demo completes")
        
    elif choice == "2":
        print("\n📊 Creating slideshow video...")
        try:
            subprocess.run([sys.executable, "demo/create_video.py"], check=True)
        except subprocess.CalledProcessError:
            print("❌ Slideshow creation failed")
    
    elif choice == "3":
        success = recorder.run_demo_with_recording()
        if success:
            print("\n🎉 Demo recording complete!")
        else:
            print("\n❌ Demo recording failed")
    
    elif choice == "4":
        create_gif_from_recording()
    
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()