shader_type canvas_item;
render_mode unshaded;

//uniform float time_factor = 1.0;


uniform vec2 tiled_factor = vec2(1.1,1.1);
uniform vec2 tiled_offset = vec2(0.05,0.05);

uniform vec2 time_scale = vec2(1.0,1.0);
uniform vec2 offset_scale = vec2(2.0,2.0);
uniform vec2 amplitude = vec2(0.05 ,0.1);

uniform float shadow_speed = 2.0;
uniform vec4 shadow_color : hint_color;

void fragment(){
	vec2 tiled_uvs = UV * tiled_factor - tiled_offset;
//	tiled_uvs.y *= aspect_ratio;
	
	vec2 waves_uv_offset;
	waves_uv_offset.x = cos(TIME * time_scale.x + (tiled_uvs.x + tiled_uvs.y) * offset_scale.x);
	waves_uv_offset.y = sin(TIME * time_scale.y + (tiled_uvs.x + tiled_uvs.y) * offset_scale.y);
	
//	vec2 waves_height_offset;
//	waves_height_offset.x = cos(TIME * time_scale.x*shadow_speed + (tiled_uvs.x + tiled_uvs.y) * offset_scale.x*4.0);
//	waves_height_offset.y = 
	
	float waves_height = sin(TIME * time_scale.y*shadow_speed + (tiled_uvs.x + tiled_uvs.y) * -offset_scale.y);
//	COLOR = vec4(waves_height,waves_height,waves_height,1.0);
//	COLOR = vec4(waves_uv_offset,0.0,1.0);
	vec4 actual_texture = texture(TEXTURE,tiled_uvs + waves_uv_offset * amplitude);
	vec4 white = vec4(1.0,1.0,1.0,1.0);
	if (actual_texture.a != 0.0 &&  waves_height >=0.9)
	{
		COLOR = mix(actual_texture,shadow_color,waves_height);
	}
	else
	{
		COLOR = actual_texture;
	}
}