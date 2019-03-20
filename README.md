# Ros_MAVRos_projects

######################### <br/>
    old_follow_color_axis --> follow_color_X_axis.py için <br/>
                              obje_pose_pub.py kodunun <br/>
                              arm servisi ve offboard modun <br/>
                              calistirlmasi gerekmetedir.<br/>
                              X ekseni yönünde nesne takip sağlandı.<br/>
                              
<br/> ******************************************************************<br/>
<br/>
roslaunch gazebo_ros empty_world.launch world_name:=$(pwd)/Tools/sitl_gazebo/worlds/iris_opt_flow.world
<br/>
no_sim=1 make px4_sitl_default gazebo_iris_opt_flow
<br/>
roslaunch mavros px4.launch fcu_url:="udp://:14540@127.0.0.1:14557"
<br/>
rosrun talker obje_pose_pub_with_cvBridge.py 
<br/>
rosrun talker follow_color.py <br/>
