tool
extends Sprite
class_name Mirror

func _ready():
	global_signal.connect("on_change_zoom",self,"_zoom_changed")
	
	if not Engine.editor_hint:
		set_process(false)

func _process(_delta):
	_zoom_changed(0) 
	
func _zoom_changed(new_zoom):
	if Engine.editor_hint:
		material.set_shader_param("y_zoom",get_viewport().global_canvas_transform.y.y)
	else:
#		print(material.get("shader_param/y_zoom"))
		var new_range = range_lerp(new_zoom.y,0,2,2,0.2)
		material.set_shader_param("y_zoom",new_zoom.y)

func _scale_changed():
	material.set_shader_param("scale",scale)
