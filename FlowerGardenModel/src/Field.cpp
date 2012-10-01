#include "Field.h"



struct FlowerConf {
    float x, y, h, rotation;
};

struct FlowersConf {
    vector<FlowerConf> flowerConfs;
};


void operator >> (const YAML::Node& node, FlowerConf& flower) {
    node["x"] >> flower.x;
    node["y"] >> flower.y;
    node["h"] >> flower.h;
    node["rotation"] >> flower.rotation;
}

void operator >> (const YAML::Node& node, FlowersConf& flowersConf) {
   const YAML::Node& flowersNode = node["flowers"];
   for(unsigned i=0;i<flowersNode.size();i++) {
        FlowerConf flowerConf;
        flowersNode[i] >> flowerConf;
        flowersConf.flowerConfs.push_back(flowerConf);
   }
}


//--------------------------------------------------------------

void Field::loadFlowers(char *fileName) {
    ifstream fin(fileName);
    YAML::Parser parser(fin);

    YAML::Node doc;
    parser.GetNextDocument(doc);

    // this is probably the worst code I've ever written

    for(unsigned int i = 0; i < doc.size(); i++) {
        FlowersConf flowersConf;
        doc >> flowersConf;
        for (unsigned int i = 0; i < flowersConf.flowerConfs.size(); i++) {
            flowers.push_back(new Flower(flowersConf.flowerConfs[i].x, flowersConf.flowerConfs[i].y, flowersConf.flowerConfs[i].h, flowersConf.flowerConfs[i].rotation));
        }
    }

//    for (int i = 0; i < 16; i++) {
//        flowers.push_back(new Flower(FIELD_WIDTH, FIELD_LENGTH));
//    }

}

//--------------------------------------------------------------
void Field::setup(){
    loadFlowers(FLOWERS_CONF);

    glEnable(GL_DEPTH_TEST);
    glEnable(GL_LIGHTING);
    glEnable(GL_LIGHT0);

    glShadeModel(GL_SMOOTH);

    GLfloat lightpos[] = {-1., -1., 0.5, 1.};
    glLightfv(GL_LIGHT0, GL_POSITION, lightpos);

    udpConnection.Create();
    udpConnection.Bind(8080);
    udpConnection.SetNonBlocking(true);
}

//--------------------------------------------------------------
void Field::update(){
    char udpMessage[512];
    int recvd = udpConnection.Receive(udpMessage, 512);

    if (recvd >= 0) {
        char *pEnd = udpMessage;
        int channels = strtol(pEnd, &pEnd, 10);
        int channel = 0;
        // TODO handle bad protocol messages
        while (pEnd < udpMessage + recvd - 1) { // -1 is fudge factor in the protocol
            int value = strtol(pEnd, &pEnd, 10);

            int flowerIdx = channel / 4;
            int lightIdx = channel % 4;

            printf("flower %d light %d brightness %d\n", flowerIdx, lightIdx, value);

            flowers[flowerIdx]->brightness[lightIdx] = value;
            channel++;
        }
    }
}

//--------------------------------------------------------------
void Field::draw(){
//    float overallBrightness = (frameCount % 1000) / 1000.0;
//    for (unsigned int i = 0; i < flowers.size(); i++) {
//        for (int j = 0; j < 4; j++) {
//            flowers[i]->brightness[j] = overallBrightness;
//        }
//    }

//    ofTranslate(ofGetWidth() / 2, 3 * ofGetHeight() / 4, 0);

    camera.begin();

    ofRotateZ(180);
    ofTranslate(0, ofGetHeight() / 6, 0);

    drawGrass();

    for (unsigned int i = 0; i < flowers.size(); i++) {
        flowers[i]->draw();
    }

    frameCount++;
}


//--------------------------------------------------------------
void Field::keyPressed(int key){

}

//--------------------------------------------------------------
void Field::keyReleased(int key){

}

//--------------------------------------------------------------
void Field::mouseMoved(int x, int y){

}

//--------------------------------------------------------------
void Field::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void Field::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void Field::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void Field::windowResized(int w, int h){

}

//--------------------------------------------------------------
void Field::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void Field::dragEvent(ofDragInfo dragInfo){

}

void Field::drawGrass() {
    GLfloat green[] = {0.f, 1.f, 0.f, 1.f};
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, green);

    glBegin(GL_QUADS);
        glNormal3i(0, 0, 1);
        glVertex3i(-FIELD_LENGTH, 0, -FIELD_WIDTH);
        glVertex3i(-FIELD_LENGTH, 0, FIELD_WIDTH);
        glVertex3i(FIELD_LENGTH, 0, FIELD_WIDTH);
        glVertex3i(FIELD_LENGTH, 0, -FIELD_WIDTH);
    glEnd();
}
