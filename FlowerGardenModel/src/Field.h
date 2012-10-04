#pragma once

#include <fstream>

#include "ofMain.h"
#include "lib/ofxNetwork/src/ofxNetwork.h"
#include "yaml.h"
#include <GL/glut.h>

#include "Flower.h"

#define FIELD_LENGTH 700
#define FIELD_WIDTH 250

#define FLOWERS_CONF "/home/boxysean/workspace/PublicConstructions/MasterControl/flowers.conf"

class Field : public ofBaseApp{
    private:
        vector<Flower*> flowers;
        ofEasyCam camera;
        int frameCount;
        ofxUDPManager udpConnection;
        int selFlowerIdx;

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

        void loadFlowers(char *fileName);
		void drawGrass();
};
