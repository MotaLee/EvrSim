#version 330 core
layout (location=0) in vec3 in_pos;
layout (location=1) in vec4 in_color;

out vec4 v_color;

uniform mat4 trans;
uniform mat4 view;
uniform mat4 projection;

uniform int highlight;

void main(){
    gl_Position =projection*view*trans*vec4(in_pos,1.0);
    if(highlight==1){
        v_color=vec4(0.5,1.0,0.7,1.0);
    }else{
        v_color = in_color;
    }
}
