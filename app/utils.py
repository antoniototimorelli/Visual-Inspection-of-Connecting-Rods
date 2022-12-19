################################################################################ 
# Antonio Morelli - 0001060348 
# utils.py - Description: 
# The functions that compute the analysis over images.
################################################################################ 
import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches as mpatches
from matplotlib import colors as cls
import random
import logging

from itertools import combinations

all_colors = ['#FF3D00', '#B2DFDB', '#F8BBD0', '#7E57C2', '#FF8A65', \
         '#FB8C00', '#A7FFEB', '#B39DDB', '#1E88E5', '#CDDC39']

# ------------------------------------------------------------------------------
# Apply median blur of kernel size 'k_s' to 'img'.
# ------------------------------------------------------------------------------
def smoothing(img, k_s):
    return cv2.medianBlur(img, k_s)

# ------------------------------------------------------------------------------
# Returns a hole object that contains the ellipse fitting the component, its
# list of countours point, its orientation, its centre coordinates and
# its diameters. 
# At the very beginning, i was trying to found the minimum enclosing circle of the contour,
# but it soon emerged that ellipses fit better the holes.
# ------------------------------------------------------------------------------
def hole_creation(component, rods):
    ellipse = cv2.fitEllipse(component['contour'])
    hole = {
        'ellipse': ellipse,
        'contour': component['contour'],
        'theta': ellipse[2],
        'centre': (round(ellipse[0][0]),round(ellipse[0][1])),
        'minor_diameter': ellipse[1][0],
        'major_diameter': ellipse[1][1]
    }

    for rod in rods:
        if cv2.pointPolygonTest(rod['contour'],hole['ellipse'][0],measureDist = False) == True:
            rod['holes'].append(hole)
            rod['type'] += 1                
            break

# ------------------------------------------------------------------------------
# Returns a rod object that contains its minimum enclosing rectangle, its
# moments values, it barycentre coordinates and width, it list of contours point, 
# its type, its orientation and its color.
# The orientation is computed according to the minimum fitting ellipse, since seemed 
# to give more accurate results. The function's call 'cv2.fitEllipse()[2]' returns
# the orientation wrt to y-axis.
#         https://datascience.stackexchange.com/questions/85064/where-is-the-rotated-angle-actually-located-in-fitellipse-method
# ------------------------------------------------------------------------------
def rod_creation(component, colors, idx_comp, rods, patches):    
    # Mer
    minRect = cv2.minAreaRect(component['contour'])
    # Moments
    moments = cv2.moments(component['contour'])

    # Barycentre
    centre = (round(moments['m10'] / moments['m00']), \
                  round(moments['m01'] / moments['m00']))
        
    rod = {
        'id': idx_comp,
        'contour': component['contour'],
        'type': 0,
        'rect': minRect,
        'cX': centre[0],
        'cY': centre[1],
        'width':  round(minRect[1][0],2),
        'length':  round(minRect[1][1],2),
        'centre_w': round(min([np.linalg.norm(centre-a) for a in component['contour']]),2),
        'color': random.choice(colors),
        'holes': [],
        'M': moments,
        'theta': cv2.fitEllipse(component['contour'])[2]
    }
    colors.remove(rod['color'])
    idx_comp += 1
    rods.append(rod)       
    patches.append(mpatches.Patch(color=cls.to_rgb(rod['color']), label = rod['id']))
    
    return rod

# ------------------------------------------------------------------------------
# Draws axes of a component, either of a rod or an of inside hole. 
# For major axis, this is done by computing the angle value wrt to the horizontal
# axis and drawing an oriented line that goes through the centre; the minor 
# axis is instead drew by rotating the major axis vector of 90° degrees.  
# ------------------------------------------------------------------------------
def draw_axis(component, output, centre, l_minor, h = False):

    (xc, yc), (d1,d2), _ = cv2.fitEllipse(component['contour'])
    angle = component['theta'] - 90 if component['theta'] > 90 else component['theta'] + 90
    
    l_major = max(d1,d2)/2
    
    xtop = xc + np.cos(np.radians(angle))       * l_major
    ytop = yc + np.sin(np.radians(angle))       * l_major
    xbot = xc + np.cos(np.radians(angle+180))   * l_major
    ybot = yc + np.sin(np.radians(angle+180))   * l_major
        
    # Drawing major axis for rods and holes
    if not h:
        cv2.line(output, (round(xtop),round(ytop)), (round(xbot),round(ybot)), (0, 255, 0), 2)
    else:
        cv2.line(output, (round(xtop),round(ytop)), (round(xbot),round(ybot)), (0, 0, 0), 1)
    
    xtop = centre[0] + np.cos(np.radians(angle+90))    * l_minor
    ytop = centre[1] + np.sin(np.radians(angle+90))    * l_minor
    xbot = centre[0] + np.cos(np.radians(angle+270))   * l_minor
    ybot = centre[1] + np.sin(np.radians(angle+270))   * l_minor
    
    # Drawing minor axis for rods and holes
    if not h:
        cv2.line(output, (round(xtop),round(ytop)), (round(xbot),round(ybot)), (0, 255, 0), 2)
                
        # Drawing barycentre
        cv2.circle(output, (centre[0], centre[1]), 5, (255, 255, 255), -1)
        cv2.circle(output, (centre[0], centre[1]), 5, (0, 0, 0), 1)
        cv2.putText(output, text = str(component['id']), org = (centre[0], centre[1]),\
            fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale = 0.6, color = (0,0,0),\
            thickness=2)
        cv2.putText(output, text = str(component['id']), org = (centre[0], centre[1]),\
                fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale = 0.6, color = (255,255,255),\
                    thickness=1)

    else:
        cv2.line(output, (round(xtop),round(ytop)), (round(xbot),round(ybot)), (0, 0, 0), 1)    

# ------------------------------------------------------------------------------
# Draws rods and their holes. 
# If debug mode is on, prints rod's features on the console.
# If 'csv' is True, then it also returns the data structure containing rods' features.
# ------------------------------------------------------------------------------
def analysis_output(filename, rods, output, rods_csv, mer = False, csv = True):
    for rod in rods:
        # Rod's type
        if rod['type'] < 2:
            logging.debug(f"\tRod: {rod['id']}-A")
        else:
            logging.debug(f"\tRod: {rod['id']}-B")

        # Filling color
        cv2.drawContours(output,[rod['contour']],-1,\
                 [ch * 256 for ch in list(cls.to_rgb(rod['color']))],thickness = cv2.FILLED)
    
        # Rod's contour
        cv2.drawContours(output,[rod['contour']],-1,\
                 (0,0,0),thickness = 1)

        # Mer
        box = cv2.boxPoints(rod['rect'])            
        box = np.int64(box)
        logging.debug(f"\t\tMER coordinates: {[(round(p[0],2),round(p[1],2))for p in box]}")
        if mer:
            cv2.drawContours(output,[box],-1,(0,0,0),1)

        # Rod's barycentre
        logging.debug(f"\t\tCentroid: ({rod['cX']}) ({rod['cY']})")
    
        # Barycentre's width
        logging.debug(f"\t\tWidth at the barycentre:' {round(rod['centre_w']*2,2)}")

        # Orientation
        logging.debug(f"\t\tTheta wrt y axis: {round(rod['theta'],2)}")
    
        # Length and width are swapped so that lenght represents always the major
        # axis of the object
        length = rod['length'] if rod['length'] > rod['width'] else rod['width']    
        width = rod['width'] if rod['width'] < rod['length'] else rod['length']
    
        logging.debug(f"\t\tWidth: {width} - Length {length}")  

        # Axis and orientation
        draw_axis(rod, output, (rod['cX'],rod['cY']), rod['centre_w'])        
        
        if csv:
            # Creation of the structure that will populate the .csv file
            rod_csv = [filename,rod['id'],'A' if rod['type'] < 2 else 'B',\
                    [(round(p[0],2),round(p[1],2))for p in box],(rod['cX'],rod['cY']),width,length,\
                    rod['centre_w'],round(rod['theta'],2),rod['color']]

            # Holes
            logging.debug(f"\t\tHoles:")
            for id_h,hole in enumerate(rod['holes']):    

                logging.debug(f"\t\t\tHole: {id_h+1}")

                # Hole's barycentre
                logging.debug(f"\t\t\t\tcentre: {hole['centre']}")    
                cv2.circle(output, hole['centre'], 2, (0, 0, 0), -1)

                # Major diameter
                logging.debug(f"\t\t\t\tMajor axis: {round(hole['major_diameter'],2)}")

                # Minor diameter
                logging.debug(f"\t\t\t\tMinor axis: {round(hole['minor_diameter'],2)}")

                # Filling color and contour
                cv2.ellipse(output,hole['ellipse'],(255,255,255),thickness = cv2.FILLED)
                cv2.ellipse(output,hole['ellipse'],(0,0,0),thickness = 1)

                # Axis and radius
                draw_axis(hole, output, hole['centre'], \
                        hole['minor_diameter']/2, True)

                rod_csv.append(hole['centre'])
                rod_csv.append(round(hole['major_diameter'],2))
                rod_csv.append(round(hole['minor_diameter'],2))
        
            # If the analyzed rod has less than two holes inside, append empty values to the data structure
            if rod['type'] < 2:
                rod_csv.append([])
                rod_csv.append(0.)
                rod_csv.append(0.)

            rods_csv.append(rod_csv)     
            
    return rods_csv
        
# ------------------------------------------------------------------------------
# Here we compute the nth-percentile (default 90) of non zero pixels in a patch 
# around the defects point to threshold the 'deepests' points (i.e. the contacts 
# point between two rods).
# ------------------------------------------------------------------------------
def percentile_nzps(contours, thresh, hierarchy, n):
    nzps = []   
    
    for c in zip(contours, hierarchy):        
        component = {
            'contour': c[0],
            'hierarchy': c[1],
        }
         
        if component['hierarchy'][2] < 0:  
            continue
        elif component['hierarchy'][3] < 0:  
            hull = cv2.convexHull(component['contour'], returnPoints = False)
            defects = cv2.convexityDefects(component['contour'],hull)
                        
            for i in range(defects.shape[0]):
                _,_,f,_ = defects[i,0]
                farthest = tuple(component['contour'][f][0])
                patch = 255-thresh[farthest[1]-5:farthest[1]+5,farthest[0]-5:farthest[0]+5]

                nzps.append(cv2.countNonZero(patch))      
    
    
    percentile = int(np.percentile(nzps, n))

    return percentile

# ------------------------------------------------------------------------------------------------
# Convexity and defects point to separate components. The key idea here is to search for convexity
# defects points of blobs' convex hull.
# A Convex object is one with no interior angles greater than 180 degrees. A shape that is not convex 
# is called Non-Convex or Concave. Hull means the exterior or the shape of the object. 
# Therefore, the Convex Hull of a shape or a group of points is a tight fitting convex boundary 
# around the points or the shape.
# Any deviation of the object from this hull can be considered as convexity defect, so what we do 
# here is find those defects points on the component countour and threshold them according to the number 
# of non zero pixels contained on the negative of the binarized image (i.e., foreground pixels) that lie 
# inside a patch taken around the defect point; it is perceptible visually that a 5x5 patch over those 
# points contains more non zero points than the rest of the possible defects points, so a threshold
# is choosen according to the value of the 90 percentile of the list of defects points ordered by
# the number of non zero points contained in their patches. 
# Source:
#   https://answers.opencv.org/question/87583/detach-blobs-with-a-contact-point/  
# ------------------------------------------------------------------------------------------------
def convexityDefects(img, thresh, contours, hierarchy, perc = 90):    
    th = percentile_nzps(contours, thresh, hierarchy, perc)
    
    for c in zip(contours, hierarchy):        
        component = {
            'contour': c[0],
            'hierarchy': c[1],
        }
         
        if component['hierarchy'][2] < 0:  
            continue
        elif component['hierarchy'][3] < 0:                      
            hull = cv2.convexHull(component['contour'], returnPoints = False)
            defects = cv2.convexityDefects(component['contour'],hull)
                        
            def_points = []
            for i in range(defects.shape[0]):
                _,_,f,_ = defects[i,0]
                farthest = tuple(component['contour'][f][0])
                patch = 255-thresh[farthest[1]-5:farthest[1]+5,farthest[0]-5:farthest[0]+5]

                nzp = cv2.countNonZero(patch)
                if nzp >= th:
                    def_points.append(farthest)
            
            for i in range(int(len(def_points)/2)):
                minimum = min([np.linalg.norm(np.array(p[0])-np.array(p[1]))\
                   for p in list(combinations(def_points,2))])
                p = [p for p in list(combinations(def_points,2)) \
                       if np.linalg.norm(np.array(p[0])-np.array(p[1])) == minimum][0]
                    
                cv2.line(thresh,p[0],p[1],(0,0,0),3)
                cv2.line(thresh,p[0],p[1],(255,255,255),2)    
                cv2.circle(thresh,p[0],2,(255,255,255),-1)    
                cv2.circle(thresh,p[1],2,(255,255,255),-1)    

                cv2.circle(img,p[0],1,(255,255,255),-1)
                cv2.circle(img,p[1],1,(255,255,255),-1)
                
                def_points.remove(p[0])
                def_points.remove(p[1])        
                
    # Finding outer and inner contours after separation
    _ , contours, hierarchy = cv2.findContours(255-thresh\
                                               , cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    return img, thresh, contours, hierarchy[0]

# ------------------------------------------------------------------------------------------------
# Analysis to discern rods contours from internal holes contours according to the hierarchy of
# their contours. 
# The 'hierarchy' variable is a three-dimensional NumPy array, with one row, X columns, and 
# a "depth" of 4. The X columns correspond to the number of contours found by the function. 
# The cv2.RETR_TREE parameter causes the function to find the internal contours as well as 
# the outermost contours for each object. Column zero corresponds to the first contour, 
# column one the second, and so on.
# Each of the columns has a four-element array of integers, representing indices of 
# other contours, according to this scheme:
#                             [next, previous, first child, parent]
# Hence, if 'first child' is equal to -1, the countour must belong to an internal hole,
# while, if it has no parent, then it must be the one of a rod.  
# Source:
#   https://stackoverflow.com/questions/11782147/python-opencv-contour-tree-hierarchy-structure
#
# Here we also take in account of possible changes of the characteristics of the working images, 
# respectively the presence of other objects like washers and screws (1), the presence of contact 
# points (2) or the one of iron powder.
# ------------------------------------------------------------------------------------------------
def component_analysis(filename, img, thresh, contours, hierarchy, output, rods_csv,\
                       change, verbose = False):  
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.CRITICAL)
            
    # By extracting hierarchy[0] we get the actual inner list of hierarchy descriptions.
    hierarchy = hierarchy[0] 
    idx_comp = 0   
    rods, patches = [],[]   
        
    colors = all_colors.copy()

    # If there are no any contact point
    if change == 2:
        img, thresh, contours, hierarchy = convexityDefects(img, thresh, contours, hierarchy, 90)    
    
    logging.debug(f"Filename: {filename}")
    for c in zip(contours, hierarchy):       
        component = {
            'contour': c[0],
            'hierarchy': c[1],
        }        
        
        # If there is iron powder, then all the  components with a surface greather than a certain threshold
        # are analyzed, while the small powder is not taken in account. 
        # I tried to use morphological operations and a stronger median filter, but it ended in corrupting
        # the shape of some rods' thins circles.
        if change == 3 and cv2.contourArea(component['contour']) <= 50:  
            continue        
        
        # If the component is an internal contour (i.e. a hole of the rod), since they do not have children 
        # in the contours hierarchy.
        if component['hierarchy'][2] < 0: 
            # If there are other objects like an elongated screw, they will not have any children in the
            # contours hierarchy too, so we threshold over circularity to avoid their analysis.
            # (A screw has lower circularity than an internal hole)
            if change == 1:
                area = cv2.contourArea(component['contour'])
                perimeter = cv2.arcLength(component['contour'],True)
                circularity = 4 * np.pi * (area / perimeter**2)

                if circularity <= 0.50:
                    continue
            
            hole_creation(component,rods)
        
        # If the component is an external contour (i.e. a rod), since they do not have parents 
        # in the contours hierarchy.       
        elif component['hierarchy'][3] < 0:
            if change == 1:
                # If there are other objects like a rounded washer, they will not have any parent in the
                # contours hierarchy too, so we threshold over circularity to avoid their analysis.
                # (A washer has higher circularity than a rod)
                area = cv2.contourArea(component['contour'])
                perimeter = cv2.arcLength(component['contour'],True)
                circularity = 4 * np.pi * (area / perimeter**2)

                if circularity > 0.85:
                    continue
            rod_creation(component, colors, idx_comp, rods, patches)
            idx_comp += 1

    # We first find all the rods, then perform the analysis
    rods_csv = analysis_output(filename, rods, output, rods_csv, csv=True)
    
    return thresh, output, rods_csv

# ------------------------------------------------------------------------------------------------
# Performing the analysis without any change.
# ------------------------------------------------------------------------------------------------
def task1(filename, filename_th, filename_o):
    img = cv2.imread(filename,0)
    rods_csv = []
    output = cv2.cvtColor(img.copy(), cv2.COLOR_GRAY2BGR)

    # Applying median blur to achieve a better binarization
    img = smoothing(img,3)
    
    # Thresholding with Otsu's method since the system should not 
    # require any change to work properly with lighting sources of different power
    _, thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    try:
    # Finding outer and inner contours
        _ , contours, hierarchy = cv2.findContours(255-thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        thresh, output, rods_csv = component_analysis(filename, img, thresh, contours,\
                hierarchy, output, rods_csv, 0) 
        
        cv2.imwrite(filename_th, 255-thresh)
        cv2.imwrite(filename_o, output)
    except:
        None

    return rods_csv

# ------------------------------------------------------------------------------------------------
# Performing the analysis with change 1, introduction of other objects.
# ------------------------------------------------------------------------------------------------
def task2_c1(filename, filename_th, filename_o):
    img = cv2.imread(filename,0)
    rods_csv = []
    output = cv2.cvtColor(img.copy(), cv2.COLOR_GRAY2BGR)

    # Applying median blur to achieve a better binarization
    img = smoothing(img,3)
    
    # Thresholding with Otsu's method since the system should not 
    # require any change to work properly with lighting sources of different power
    _, thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    try:
    # Finding outer and inner contours
        _ , contours, hierarchy = cv2.findContours(255-thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        thresh, output, rods_csv = component_analysis(filename, img, thresh, contours, hierarchy, output, rods_csv, 1) 

        cv2.imwrite(filename_th, 255-thresh)
        cv2.imwrite(filename_o, output)
    except:
        None

    return rods_csv

# ------------------------------------------------------------------------------------------------
# Performing the analysis with change 2, introduction of contact points between rods.
# ------------------------------------------------------------------------------------------------
def task2_c2(filename, filename_th, filename_o):
    img = cv2.imread(filename,0)
    rods_csv = []
    output = cv2.cvtColor(img.copy(), cv2.COLOR_GRAY2BGR)

    # Applying median blur to achieve a better binarization
    img = smoothing(img,3)
    
    # Thresholding with Otsu's method since the system should not 
    # require any change to work properly with lighting sources of different power
    _, thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    try:
    # Finding outer and inner contours
        _ , contours, hierarchy = cv2.findContours(255-thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        thresh, output, rods_csv = component_analysis(filename, img, thresh, contours, hierarchy, output, rods_csv, 2) 

        cv2.imwrite(filename_th, 255-thresh)
        cv2.imwrite(filename_o, output)
    except:
        None

    return rods_csv

# ------------------------------------------------------------------------------------------------
# Performing the analysis with change 1, introduction of scattered iron powder.
# ------------------------------------------------------------------------------------------------
def task2_c3(filename, filename_th, filename_o):
    img = cv2.imread(filename,0)
    rods_csv = []
    output = cv2.cvtColor(img.copy(), cv2.COLOR_GRAY2BGR)

    # Applying median blur to achieve a better binarization
    img = smoothing(img,3)
    
    # Thresholding with Otsu's method since the system should not 
    # require any change to work properly with lighting sources of different power
    _, thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    try:
    # Finding outer and inner contours
        _ , contours, hierarchy = cv2.findContours(255-thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        thresh, output, rods_csv = component_analysis(filename, img, thresh, contours, hierarchy, output, rods_csv, 3) 

        cv2.imwrite(filename_th, 255-thresh)
        cv2.imwrite(filename_o, output)
    except:
        None

    return rods_csv
