import processing.video.*;

Capture video;
boolean freezeFrame = false;
PImage frozenImage;
boolean canTakePhoto = true;
long photoStartTime = 0;
int freezeDelay = 4000;

boolean canDetect = true;
boolean startTime = false;

boolean reset = false;
long resetStartTime = 0;
int resetDelay = 5000;

int resolutionX = 640;
int resolutionY = 480;
float motionThreshold = 10;

int timer = 0;


void setup() {
  fullScreen();
  
  noCursor();

  video = new Capture(this, resolutionX, resolutionY, 15);
  video.start();
}

void captureEvent(Capture video) {
  video.read();
  PImage currentFrame = video.get();
  if(keyPressed){
    if(key == 'g') {
      if(canTakePhoto){
        freezeFrame = false;
        photoStartTime = millis();
        startTime = true;
        canTakePhoto = false;
      }
    }
  }
  if(startTime)
  {
    timer = (int) abs((millis() - photoStartTime) - 4000);
    
    if(millis() - photoStartTime >= freezeDelay) {
      freezeFrame = true;
      frozenImage = currentFrame;
      
      canTakePhoto = true;
      startTime = false;
    }
  }
}

void draw() {
  background(0);
  // Scale the video feed to fit the screen
  float aspectRatio = float(resolutionX) / resolutionY;
  float newWidth = width;
  float newHeight = width / aspectRatio;
  
  if (newHeight > height) {
    newHeight = height;
    newWidth = height * aspectRatio;
  }
  
  // Calculate the x and y offsets to center the image
  float offsetX = (width - newWidth) / 2;
  float offsetY = (height - newHeight) / 2;

  if (freezeFrame && frozenImage != null) {
    image(frozenImage, offsetX, offsetY, newWidth, newHeight);
    filter(BLUR, 1.5);
    filter(THRESHOLD);
  } else {
    image(video, offsetX, offsetY, newWidth, newHeight);
  }
  
  textSize(128);
  fill(#FF0000);
  
  if(startTime)
  {
    text(str(timer / 1000), 30, displayHeight - 50);
  } else {
    text("", 0, 0);
  }
}
