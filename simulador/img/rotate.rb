img = "robot_led_on.png"
name = img.split('.')[0]
(0..35).each{ |x|
	`convert #{img} -background "transparent" -rotate #{x*10} #{name}-#{x}.png`
}