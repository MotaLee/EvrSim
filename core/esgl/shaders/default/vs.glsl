layout (location=0) in vec3 pos;
layout (location=1) in vec4 color;
layout (location=2) in vec2 tex;

out vec4 vtx_color;
out vec2 tex_cs;

void main(){
    tex_cs=vec2(0,0);
    gl_Position =proj*view*trans*vec4(pos,1.0);
    if(flags.has_tex==1) tex_cs=tex;
    vtx_color=color;
}
