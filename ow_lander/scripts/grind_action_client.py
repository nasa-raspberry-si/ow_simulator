#!/usr/bin/env python2

# The Notices and Disclaimers for Ocean Worlds Autonomy Testbed for Exploration
# Research and Simulation can be found in README.md in the root directory of
# this repository.

import rospy
import actionlib
import ow_lander.msg
import constants
import argparse

def Grind_client():
    parser = argparse.ArgumentParser()
    parser.add_argument('x_start', type=float, help='X coordinate of grinding starting point', nargs='?', default=1.65, const=0)
    parser.add_argument('y_start', type=float, help='Y coordinate of grinding starting point', nargs='?', default=0.0, const=0)
    parser.add_argument('depth', type=float, help='Desired depth', nargs='?', default=0.05, const=0)
    parser.add_argument('length', type=float, help='Desired length', nargs='?', default=0.6, const=0)
    parser.add_argument('parallel', type=bool, help='If True, resulting trench is parallel to arm. If False, perpendicular to arm', nargs='?', default=1, const=0)
    parser.add_argument('ground_position', type=float, help='Desired length', nargs='?', default=constants.DEFAULT_GROUND_HEIGHT, const= 0 )
    args = parser.parse_args()
    rospy.loginfo("Requetsed x_start: %s", args.x_start)
    rospy.loginfo("Requetsed y_start: %s", args.y_start)
    rospy.loginfo("Requetsed depth: %s", args.depth)
    rospy.loginfo("Requetsed length: %s", args.length)
    rospy.loginfo("Requetsed parallel: %s", args.parallel)
    rospy.loginfo("Requetsed ground_position: %s", args.ground_position)
 
    client = actionlib.SimpleActionClient('Grind', ow_lander.msg.GrindAction)

    client.wait_for_server()

    goal = ow_lander.msg.GrindGoal()
    
    goal.x_start = args.x_start 
    goal.y_start = args.y_start
    goal.depth = args.depth
    goal.length = args.length
    goal.parallel = args.parallel
    goal.ground_position = args.ground_position

    # Default trenching values
    
    # goal.x_start = 1.65
    # goal.y_start = 0.0
    # goal.depth = 0.05
    # goal.length = 0.6 # 0.6
    # goal.parallel = False
    # goal.ground_position = constants.DEFAULT_GROUND_HEIGHT

    # General trenching values for non- parallel circular/linear trenching     
    #goal.x_start = 1.55
    #goal.y_start = 0.1
    #goal.depth = 0.045
    #goal.length = 0.5 # 0.6 
    #goal.parallel = False
    #goal.ground_position = -0.155

    # General trenching values for linear trenching            
    #goal.x_start = 1.65
    #goal.y_start = 0.2
    #goal.depth = 0.045
    ##choose a generous value for goal length to avoid collision
    #goal.length = 0.7  
    #goal.parallel = True
    #goal.ground_position = -0.155

    # Sends the goal to the action server.
    client.send_goal(goal)

    # Waits for the server to finish performing the action.
    client.wait_for_result()

    # Prints out the result of executing the action
    return client.get_result()  # 

if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the grind can
        # publish and subscribe over ROS.
        rospy.init_node('Grind_client_py')
        result = Grind_client()
        rospy.loginfo("Result: %s", result)
    except rospy.ROSInterruptException:
        rospy.logerror("program interrupted before completion")
