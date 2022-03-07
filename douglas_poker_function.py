import numpy as np
from shapely.geometry import Point
import pandas as pd
from pandasql import sqldf

# get the utm points
def get_points(land):
    global boundsxy
    global all_points
    global rowdata
    global data
    global new_data
    mysql = lambda q: sqldf(q, globals()) 
   
    ### get first point: it's a point with maximum distance from center
    center=land.centroid
    x_center=center.x
    y_center=center.y
    points_all=list(land.exterior.coords)
    all_points=pd.DataFrame(points_all,columns=['x','y'])
    all_points['d_center']=np.sqrt((all_points['x']-x_center)**2+(all_points['y']-y_center)**2) 

    query='''
    SELECT max(d_center) dist1,ROUND(x,2) x,ROUND(y,2) y
    from  all_points ;
    '''

    point1=mysql(query)
    p1=Point(point1.x,point1.y)


    ### get secend point: it's a point with maximum distance from first point
    all_points['d_p1']=np.sqrt((all_points['x']-p1.x)**2+(all_points['y']-p1.y)**2)

    query='''
    SELECT max(d_p1) dist2,ROUND(x,2) x,ROUND(y,2) y
    from  all_points ;
    '''

    point2=mysql(query)
    p2=Point(point2.x,point2.y)


    ### get third point: it's a point with maximum distance from line between point 1,2
    # point distance from the line between points 1,2
    if (p2.x-p1.x)==0:
        m=99999
    else:
        m=(p2.y-p1.y)/(p2.x-p1.x)
    c=m*-p1.x+p1.y
    lenght=np.sqrt(m**2+1**2)
    all_points['xy_d1']=np.abs(m*all_points['x'] - all_points['y']+c)/lenght

    query='''
    SELECT max(xy_d1) dist3,ROUND(x,2) x,ROUND(y,2) y
    from  all_points ;
    '''
    point3=mysql(query)
    p3=Point(point3.x,point3.y)

    ### get fourt point: it's a point with maximum distance from lines between point 1,2,3
    # point distance from the line between points 1,3
    if (p3.x-p1.x)==0:
        m2=99999
    else:
        m2=(p3.y-p1.y)/(p3.x-p1.x)
    c2=m2*-p1.x+p1.y
    lenght2=np.sqrt(m2**2+1**2)
    all_points['xy_d2']=np.abs(m2*all_points['x'] - all_points['y']+c2)/lenght2
    # point distance from the line between points 2,3
    if (p2.x-p3.x)==0:
        m3=99999
    else:
        m3=(p2.y-p3.y)/(p2.x-p3.x)
    c3=m3*-p3.x+p3.y
    lenght3=np.sqrt(m3**2+1**2)
    all_points['xy_d3']=np.abs(m3*all_points['x'] - all_points['y']+c3)/lenght3


    query='''
    SELECT max(min(xy_d1,xy_d2,xy_d3)) result,ROUND(x,2) x,ROUND(y,2) y
    from  all_points ;
    '''

    point4=mysql(query)
    p4=Point(point4.x,point4.y)

    # organizing the result   
    point_id=['1','2','3','4']
    point_xx=[p1.x,p2.x,p3.x,p4.x]
    point_yy=[p1.y,p2.y,p3.y,p4.y]
    border_points = pd.DataFrame(data={'point_id':point_id,'x':point_xx,'y':point_yy})
    return(border_points)
