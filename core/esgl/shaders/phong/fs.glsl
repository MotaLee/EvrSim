in vec4 vtx_color;
in vec2 tex_cs;
in vec3 vtx_normal;
in vec3 frag_pos;
out vec4 FragColor;
float COFF_AMBIENT=0.2;
float COFF_SPECULAR = 0.5;
vec3 calPointLight(Light l);

void main(){
    vec4 base_color;
    if(flags.is_highlight==1){
        FragColor=vec4(0.5,1.0,0.7,1.0);
    }else if(flags.is_frame==1){
        FragColor= vec4(1.0,1.0,1.0,1.0);
    }else{
        if(flags.has_tex==1){
            base_color=texture(id_tex,tex_cs);
        }else{
            base_color=vtx_color;
        }

        vec3 result=vec3(0.,0.,0.);
        vec3 ret;
        for(int i=0;i<NUM_LIGHTS;i++){
            if(lights[i].type==1){
                ret=calPointLight(lights[i]);
                result+=ret;
            }
        }
        FragColor=vec4(vec3(result*base_color),1.);
    }

}

vec3 calPointLight(Light l){
    vec3 ambient = COFF_AMBIENT*l.color;

    vec3 lgt_dir=normalize(l.pos - frag_pos);
    float diff = max(dot(vtx_normal,lgt_dir), 0.0);
    vec3 diffuse = l.strength*diff*l.color;

    vec3 view_dir=normalize(pos_eye-frag_pos);
    vec3 reflect_dir = reflect(-lgt_dir, vtx_normal);
    float spec = pow(max(dot(view_dir, reflect_dir), 0.0), 32);
    vec3 specular = COFF_SPECULAR * spec * l.color;
    return ambient+diffuse+specular;
}
