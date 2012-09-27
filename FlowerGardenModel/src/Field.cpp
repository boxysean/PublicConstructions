#include "Field.h"

//--------------------------------------------------------------
void Field::setup(){
    for (int i = 0; i < 5; i++) {
        flowers.push_back(new Flower(FIELD_WIDTH, FIELD_LENGTH));
    }

    glEnable(GL_DEPTH_TEST);
    glEnable(GL_LIGHTING);
    glEnable(GL_LIGHT0);

    glShadeModel(GL_SMOOTH);

    GLfloat lightpos[] = {1., 1., 0, 1.};
    glLightfv(GL_LIGHT0, GL_POSITION, lightpos);
    GLfloat lightpos2[] = {1., 0., 0.5, 1.};
    glLightfv(GL_LIGHT1, GL_POSITION, lightpos2);

    udpConnection.Create();
    udpConnection.Bind(8080);
    udpConnection.SetNonBlocking(true);
}

//--------------------------------------------------------------
void Field::update(){
    char udpMessage[512];
    int recvd = udpConnection.Receive(udpMessage, 512);
    string message = udpMessage;

    if (recvd >= 0 || message != "") {
        cout << "received: " << message << " " << recvd << endl;
    }
}

//--------------------------------------------------------------
void Field::draw(){
    float overallBrightness = (frameCount % 1000) / 1000.0;
    for (unsigned int i = 0; i < flowers.size(); i++) {
        for (int j = 0; j < 4; j++) {
            flowers[i]->brightness[j] = overallBrightness;
        }
    }

    ofTranslate(ofGetWidth() / 2, 3 * ofGetHeight() / 4, 0);

    camera.begin();

    ofRotateZ(180);
    ofTranslate(0, ofGetHeight() / 4, 0);

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
