import processing.video.*;

Capture video;
PImage prevFrame;
boolean freezeFrame = false;
PImage frozenImage;
boolean motionDetected = false;
long motionStartTime = 0;
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
  
  
  if (prevFrame != null) {
    PImage currentFrame = video.get();
     
    float motion = detectMotion(prevFrame, currentFrame);
    
    
    if(canDetect)
    {
      if (motion > motionThreshold) 
      {
       
          freezeFrame = false;
          
          if(!motionDetected) 
          {
            
            motionStartTime = millis();
            startTime = true;
            motionDetected = true;
            
          }
      }
      // don't trigger photo unless motion is detected
      if(startTime)
      {
        timer = (int)  abs((millis() - motionStartTime) - 4000);
       
        if(millis() - motionStartTime >= freezeDelay) {
          
          // freeze current image
          freezeFrame = true;
          frozenImage = currentFrame;
          
          // reset everything and kick out of detection logic
          startTime = false;
          motionDetected = false;
          canDetect = false;
        }
      }
    } else { // after photo is taken
      if(motion < motionThreshold) {
        
        if(!reset)
        {
          resetStartTime = millis();
          reset = true;
        }
        //print(millis() - resetStartTime + "\n");
        if(reset && millis() - resetStartTime >= resetDelay)
        {
          // reset so that motion can be detected again and photo can get replaced
          
          resetStartTime = 0; 
          motionDetected = false;
          canDetect = true;
          reset = false;
        }
      } else {
        resetStartTime = 0;
        reset = false;
      }
    }
  prevFrame = currentFrame;
  } else {
    prevFrame = video.get();
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
    filter(BLUR, 1.3);
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

float detectMotion(PImage prev, PImage curr) {
  prev.loadPixels();
  curr.loadPixels();
  
  float totalMotion = 0;
  
  for (int i = 0; i < curr.pixels.length; i++) {
    color c1 = curr.pixels[i];
    color c2 = prev.pixels[i];
    
    float r1 = red(c1), g1 = green(c1), b1 = blue(c1);
    float r2 = red(c2), g2 = green(c2), b2 = blue(c2);
    
    float diff = dist(r1, g1, b1, r2, g2, b2);
    totalMotion += diff;
  }
  
  return totalMotion / curr.pixels.length;
}
