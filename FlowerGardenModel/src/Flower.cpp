#include "Flower.h"

#include "ofMain.h"
#include "ofConstants.h"

static int dx[] = { 1, 0, -1, 0 };
static int dy[] = { 0, -1, 0, 1 };

Flower::Flower(double xx, double yy, double hh) {
    x = xx;
    z = yy;
    h = hh;
    stemWidth = FLOWER_STEM_WIDTH;
    orientation = ofRandom(180);

    for (int i = 0; i < 4; i++) {
        brightness[i] = 0;
    }
}

Flower::Flower(double xrange, double zrange) {
    x = ofRandom(-xrange, xrange);
    z = ofRandom(-zrange, zrange);
    h = ofRandom(FLOWER_STEM_MIN_SIZE, FLOWER_STEM_MAX_SIZE);
    stemWidth = FLOWER_STEM_WIDTH;
    orientation = ofRandom(180);

    for (int i = 0; i < 4; i++) {
        brightness[i] = 0;
    }
}

void Flower::draw() {
    ofPushMatrix();

    ofTranslate(x, 0, z);

    // --- Draw the stem ---

    ofPushMatrix();

    GLUquadric* quad = gluNewQuadric();
    // tell GLU how to create the cylinder
    gluQuadricNormals(quad, GLU_SMOOTH);
    gluQuadricDrawStyle(quad, GLU_FILL);
    gluQuadricOrientation(quad, GLU_OUTSIDE); // generates normal for quadric
    ofRotateX(90);

    GLfloat grey[] = {.75f, .75f, .75f, 1.f};
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, grey);

    gluCylinder(quad, stemWidth, stemWidth, h, FLOWER_STEM_SLICES, 1);

    ofPopMatrix();

    // --- Draw the flower ---

    ofPushMatrix();
    ofTranslate(0, -h, 0);

    ofRotateY(orientation);

    ofRotateZ(45);

    GLfloat white[] = {1.f, 1.f, 1.f, 1.f};
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, white);

    ofPushMatrix();
    ofScale(1, 1, 0.6);
    ofBox(0, 0, 0, FLOWER_HEAD_SIZE);
    ofPopMatrix();

    gluQuadricOrientation(quad, GLU_OUTSIDE); // generates normal for quadric

//    GLfloat whitez[] = {0.8f, 0.8f, 0.8f, 1.0f};
//    GLfloat cyan[] = {0.f, .8f, .8f, 1.f};
//    glMaterialfv(GL_FRONT, GL_DIFFUSE, cyan);
//    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, whitez);
    GLfloat shininess[] = {50};
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, shininess);


    for (int i = 0; i < 4; i++) {
        GLfloat yellow[] = {brightness[i] / 255.f, brightness[i] / 255.f, 0.f, 1.f};
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, yellow);

        ofPushMatrix();
        ofTranslate(dx[i] * FLOWER_PETAL_RADIUS*2, dy[i] * FLOWER_PETAL_RADIUS*2, -FLOWER_PETAL_WIDTH/2);
        gluCylinder(quad, FLOWER_PETAL_RADIUS, FLOWER_PETAL_RADIUS, FLOWER_PETAL_WIDTH, FLOWER_PETAL_SLICES, 1);
        gluDisk(quad, 0, FLOWER_PETAL_RADIUS, FLOWER_PETAL_SLICES, 1);
        ofTranslate(0, 0, FLOWER_PETAL_WIDTH);
        gluDisk(quad, 0, FLOWER_PETAL_RADIUS, FLOWER_PETAL_SLICES, 1);
        ofPopMatrix();
    }

    gluDeleteQuadric(quad);

    ofPopMatrix();

    ofPopMatrix();
}
