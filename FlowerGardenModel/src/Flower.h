#ifndef FLOWER_H_INCLUDED
#define FLOWER_H_INCLUDED

#define FLOWER_STEM_SLICES 20
#define FLOWER_STEM_MIN_SIZE 50
#define FLOWER_STEM_MAX_SIZE 250
#define FLOWER_STEM_WIDTH 5

#define FLOWER_PETAL_SLICES 20
#define FLOWER_PETAL_RADIUS 10
#define FLOWER_PETAL_WIDTH 4

#define FLOWER_HEAD_SIZE 15

class Flower {
    public:
        double x, z, h;
        double stemWidth;
        double orientation;
        int brightness[4];

        Flower(double xrange, double zrange);
        void draw();
};

#endif // FLOWER_H_INCLUDED
