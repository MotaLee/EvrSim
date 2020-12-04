#version 330 core
uniform int has_texture;
uniform int wireframe;
uniform int highlight;
uniform sampler2D texture_id;
out vec4 FragColor;
in vec4 v_color;
in vec2 tex_coord;
void main(){
    if(highlight==1){
        FragColor=vec4(0.5,1.0,0.7,1.0);
    }else if(has_texture==1){
        FragColor = texture(texture_id,tex_coord);
    }else if(wireframe==1){
        FragColor = vec4(1.0,1.0,1.0,1.0);
    }else{
        FragColor=v_color;
    }
}
