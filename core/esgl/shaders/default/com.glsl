#version 330 core

struct Flag {
    int has_tex;
    int has_color;
    int is_frame;
    int is_highlight;
};

uniform Flag flags;
uniform mat4 trans;
uniform mat4 view;
uniform mat4 proj;
uniform sampler2D id_tex;
