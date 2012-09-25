#include "Flower.h"

#include "ofMain.h"
#include "ofConstants.h"

static int dx[] = { 1, 0, -1, 0 };
static int dy[] = { 0, -1, 0, 1 };

Flower::Flower(double xrange, double zrange) {
    x = ofRandom(-xrange, xrange);
    z = ofRandom(-zrange, zrange);
    h = ofRandom(FLOWER_STEM_MIN_SIZE, FLOWER_STEM_MAX_SIZE);
    stemWidth = FLOWER_STEM_WIDTH;
    orientation = ofRandom(360);
}

void Flower::draw() {
    ofPushMatrix();

    ofTranslate(x, 0, z);


    ofPushMatrix();

    ofSetColor(ofColor::gray);

    GLUquadric* quad = gluNewQuadric();
    // tell GLU how to create the cylinder
//    gluQuadricNormals(quad, GLU_SMOOTH);
//    gluQuadricDrawStyle(quad, GLU_FILL);
//    gluQuadricTexture(quad, GL_TRUE);
//    gluQuadricOrientation(quad, GLU_OUTSIDE);
    ofRotateX(90);

    gluCylinder(quad, stemWidth, stemWidth, h, FLOWER_STEM_SLICES, 1);

    gluDeleteQuadric(quad);

    ofPopMatrix();

    ofPushMatrix();
    ofTranslate(0, -h, 0);

    ofRotateY(orientation);

    ofRotateZ(45);

    ofSetColor(ofColor::white);
    ofBox(0, 0, 0, FLOWER_HEAD_SIZE);

    GLUquadric* quad2 = gluNewQuadric();

    ofSetColor(ofColor::yellow);

    for (int i = 0; i < 4; i++) {
        // maybe do a rotation...? for some flowers..
        ofPushMatrix();
        ofTranslate(dx[i] * FLOWER_PETAL_RADIUS*2, dy[i] * FLOWER_PETAL_RADIUS*2, -FLOWER_PETAL_WIDTH/2);
        gluCylinder(quad2, FLOWER_PETAL_RADIUS, FLOWER_PETAL_RADIUS, FLOWER_PETAL_WIDTH, FLOWER_PETAL_SLICES, 1);
        ofCircle(0, 0, FLOWER_PETAL_RADIUS);
        ofPopMatrix();
    }

    gluDeleteQuadric(quad2);

    ofPopMatrix();

    ofPopMatrix();
}
