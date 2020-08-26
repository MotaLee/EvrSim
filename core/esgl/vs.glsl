// #version 330 core
layout (location=0) in vec3 in_pos;
layout (location=1) in vec4 in_color;
layout (location = 2) in vec2 in_texture;

out vec4 v_color;
out vec2 tex_coord;

uniform mat4 trans;
uniform mat4 view;
uniform mat4 projection;
uniform int has_texture;

void main(){
    gl_Position =projection*view*trans*vec4(in_pos,1.0);
    if(has_texture==1){
        tex_coord=in_texture;
    }else{
        tex_coord=vec2(0,0);
    }
    v_color=in_color;
}
