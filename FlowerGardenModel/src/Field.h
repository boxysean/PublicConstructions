#pragma once

#include "ofMain.h"
#include "src/Flower.h"

#define FIELD_LENGTH 100
#define FIELD_WIDTH 100

class Field : public ofBaseApp{
    private:
        vector<Flower*> flowers;
        ofEasyCam camera;

	public:
		void setup();
		void update();
		void draw();

		void keyPressed(int key);
		void keyReleased(int key);
		void mouseMoved(int x, int y);
		void mouseDragged(int x, int y, int button);
		void mousePressed(int x, int y, int button);
		void mouseReleased(int x, int y, int button);
		void windowResized(int w, int h);
		void dragEvent(ofDragInfo dragInfo);
		void gotMessage(ofMessage msg);

		void drawGrass();
};
