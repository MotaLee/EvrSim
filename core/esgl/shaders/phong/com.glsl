#version 330 core
#define NUM_LIGHTS 2

struct Flag {
    int has_tex;
    int has_color;
    int is_frame;
    int is_highlight;
};

struct Light {
    int type;
    vec3 pos;
    vec3 color;
    float strength;
};

uniform Flag flags;
uniform Light lights[NUM_LIGHTS];
uniform mat4 trans;
uniform mat4 view;
uniform mat4 proj;
uniform sampler2D id_tex;
uniform vec3 pos_eye;
