#include "Field.h"

//--------------------------------------------------------------
void Field::setup(){
    for (int i = 0; i < 5; i++) {
        flowers.push_back(new Flower(FIELD_WIDTH, FIELD_LENGTH));
    }

    glEnable(GL_DEPTH_TEST);
}

//--------------------------------------------------------------
void Field::update(){

}

//--------------------------------------------------------------
void Field::draw(){
    unsigned int i;

    ofTranslate(ofGetWidth() / 2, 3 * ofGetHeight() / 4, 0);

    camera.begin();

    ofRotateZ(180);
    ofTranslate(0, ofGetHeight() / 4, 0);

    drawGrass();

    for (i = 0; i < flowers.size(); i++) {
        flowers[i]->draw();
    }
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
    ofSetColor(ofColor::green);

    glBegin(GL_QUADS);
        glVertex3i(-FIELD_LENGTH, 0, -FIELD_WIDTH);
        glVertex3i(-FIELD_LENGTH, 0, FIELD_WIDTH);
        glVertex3i(FIELD_LENGTH, 0, FIELD_WIDTH);
        glVertex3i(FIELD_LENGTH, 0, -FIELD_WIDTH);
    glEnd();
}
