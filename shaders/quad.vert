#version 330 core


layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_color;

uniform mat4 model;
uniform mat4 proj;
uniform mat4 view;

out vec3 color;

void main(){
    color = in_color;
    gl_Position = proj * view * model * vec4(in_position, 1);
}