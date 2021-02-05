in vec4 vtx_color;
in vec2 tex_cs;
out vec4 FragColor;

void main(){
    if(flags.is_highlight==1){
        FragColor=vec4(0.5,1.0,0.7,1.0);
    }else if(flags.is_frame==1){
        FragColor = vec4(1.0,1.0,1.0,1.0);
    }else if(flags.has_tex==1){
        FragColor = texture(id_tex,tex_cs);
    }else{
        FragColor=vtx_color;
    }
}
