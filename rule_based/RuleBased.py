# RuleBased.py

import numpy as np
import cv2
import time, datetime, os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as dynamic_plt

# A Rule Based approach to Autonomy with my RC Car
class RuleBased:
    def __init__(self):
        # random access storage
        self.storage_frame = 'storage/current_frame.pickle'
        self.storage_curve = 'storage/current_lane_radius.pickle'
        self.storage_decision = 'storage/current_decision.pickle'
        
        # frame info
        self.width = 320
        self.height = 240
        self.required_channels = 1
        self.dtype = np.uint8

        # roi (region of interest) constants
        self.roi_vertices = np.array([[35, self.height - 1], [115, 160],
                                      [200, 160], [300, self.height - 1]],
                                     dtype=np.int32)
        self.mask = np.zeros((self.height, self.width), dtype=self.dtype)

        # warp constants
        self.warp_points= np.float32([[130, 160], [195, 160],
                                      [25, self.height], [310, self.height]])
        self.frame_points = np.float32([[0,0], [self.width,0],
                                       [0, self.height], [self.width, self.height]])
        self.warp_matrix = cv2.getPerspectiveTransform(self.warp_points, self.frame_points)
        self.frame_matrix = cv2.getPerspectiveTransform(self.frame_points, self.warp_points)

        # curve-fit constants
        self.no_windows = 15
        self.window_height = self.height // self.no_windows
        self.margin = 25
        self.minimum_relevant_pixels = 1
        self.difference_threshold = 500
        self.curvature_value = None

        # meter to pixel
        self.ym_per_pix = 30 / self.height
        self.xm_per_pix = 4 / self.width
        self.y_evaluation = self.height * (30 / self.height)
        
    def preprocess(self, image):
        # grey scale & edge
        image = cv2.Canny(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), threshold1=100, threshold2=200)
        
        # fill the mask (black)
        self.mask = np.zeros_like(image)
        cv2.fillPoly(self.mask, [self.roi_vertices], 255)
        
        # return roi image
        return image

    def un_distort(self, image):
        # skip (for now)
        return image

    def warp(self, image):
        # warp image
        warped_image = cv2.warpPerspective(image, self.warp_matrix, (self.width, self.height))

        # historgram peaks (average of where left & right lane is)
        histogram = np.sum(warped_image[warped_image.shape[0] // 2:,:], axis=0)
        print(histogram)
        # midpoint index
        midpoint = int(histogram.shape[0] / 2)
        
        # left lane (average), right lane (average)
        histogram_peaks = [np.argmax(histogram[:midpoint]), # max(values before midpoint)
                           np.argmax(histogram[midpoint:])  # max(values after midpoint)
                           + midpoint]
        
        return warped_image, histogram_peaks

    def curve_fit(self, image, histogram_peaks, draw_windows=True,
                  lane_design = 'fill', show_windows=False): # fill | dotted-curve
        left_lane_indeces = []
        right_lane_indeces = []

        # storing all white (255) pixels
        nonzero = image.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        # make rgb template of image & OG copy
        template = np.dstack((image, image, image)) * 255
        og_warped = image.copy()

        # store histogram peaks (l-avg, r-avg)        
        current_left_average = histogram_peaks[0]
        current_right_average = histogram_peaks[1]

        # iterate over sliding windows
        for window in range(self.no_windows):
            # find window boundaries (x,y) on left, right
            y_low = image.shape[0] - (window + 1) * self.window_height
            y_high = image.shape[0] - window * self.window_height
            x_left_low = current_left_average - self.margin
            x_left_high = current_left_average + self.margin
            x_right_low = current_right_average - self.margin
            x_right_high = current_right_average + self.margin

            # draw windows in template
            if draw_windows:
                # left side
                cv2.rectangle(template, (x_left_low, y_low), (x_left_high, y_high),
                              (100, 255, 255), 1)
                # right side
                cv2.rectangle(template, (x_right_low, y_low), (x_right_high, y_high),
                              (100, 255, 255), 1)
            
            # identify relevant (white => 255)pixels inside drawn windows
            relevant_left_indeces = ((nonzeroy >= y_low) & (nonzeroy < y_high) # (x,y) boundary
                                     & (nonzerox >= x_left_low) & (nonzerox < x_left_high)).nonzero()[0] # 255 (white) only
            relevant_right_indeces = ((nonzeroy >= y_low) & (nonzeroy < y_high) # (x,y) boundary
                                      & (nonzerox >= x_right_low) & (nonzerox < x_right_high)).nonzero()[0] # 255 (white) only

            # store relevant (in boundary) pixel indeces
            left_lane_indeces.append(relevant_left_indeces)
            right_lane_indeces.append(relevant_right_indeces)

            # recenter next window using relevant pixel mean
            if len(relevant_left_indeces) > self.minimum_relevant_pixels:
                current_left_average = np.int(np.mean(nonzerox[relevant_left_indeces]))
            if len(relevant_right_indeces) > self.minimum_relevant_pixels:    
                current_right_average = np.int(np.mean(nonzerox[relevant_right_indeces]))

        # concatenate (join) all relevant indeces
        left_lane_indeces = np.concatenate(left_lane_indeces)
        right_lane_indeces = np.concatenate(right_lane_indeces)

        if show_windows:
            cv2.imshow('WINDOW FRAME', template)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # store (x,y) positions of left & right lane
        left_xs = nonzerox[left_lane_indeces]
        left_ys = nonzeroy[left_lane_indeces]
        right_xs = nonzerox[right_lane_indeces]
        right_ys = nonzeroy[right_lane_indeces]

        print(len(left_xs), len(left_ys))
        print(len(right_xs), len(right_ys))
    
        # fit quadratic equation to lanes
        pixel_left_quadratic = np.polyfit(left_ys, left_xs, 2)
        pixel_right_quadratic = np.polyfit(right_ys, right_xs, 2)

        # get a,b,c <-- ax^2 + bx + c --> (quadratic equation)
        left_coefficient_a = [pixel_left_quadratic[0]]
        left_coefficient_b = [pixel_left_quadratic[1]]
        left_c = [pixel_left_quadratic[2]]
        right_coefficient_a = [[pixel_right_quadratic[0]]]
        right_coefficient_b = [pixel_right_quadratic[1]]
        right_c = [pixel_right_quadratic[2]]

        # generate (x,y) space for plotting
        plot = np.linspace(0, image.shape[0] - 1, image.shape[0])
        template[nonzeroy[left_lane_indeces], nonzerox[left_lane_indeces]] = \
                                              [255, 0, 100]
        template[nonzeroy[right_lane_indeces], nonzerox[right_lane_indeces]] = \
                                               [0, 100, 255]

        # meter quadratic
        meter_left_quadratic = np.polyfit(left_ys * self.ym_per_pix, left_xs * self.xm_per_pix, 2)
        meter_right_quadratic = np.polyfit(right_ys * self.ym_per_pix, right_xs * self.xm_per_pix, 2)

        # curvature radius of parabola (using calculus)
        # roc = [[1 + (dy / dx)^2]^3/2] / |(d^2 * y) / d * x^2|
        curve_radius = ((1 + (2 * meter_left_quadratic[0] * self.y_evaluation +
                                      meter_left_quadratic[1]) ** 2) ** 1.5)\
                               / np.absolute(2 * meter_left_quadratic[0])

        print(f"Radius of curvature: {self.curvature_value}")
        
        blank_warped = np.zeros_like(og_warped).astype(np.uint8) # 0 => black warped
        colour_warped = np.dstack((blank_warped, blank_warped, blank_warped)) # coloured blank_warped
        
        if lane_design == 'fill':
            # generate (x,y) values to plot
            left_fit = pixel_left_quadratic[0] * plot ** 2 + pixel_left_quadratic[1] \
                       * plot + pixel_left_quadratic[2]
            right_fit = pixel_right_quadratic[0] * plot ** 2 + pixel_right_quadratic[1] \
                        * plot + pixel_right_quadratic[2]

            # recast (x,y) values for cv
            left_lane_points = np.array([np.transpose(np.vstack([left_fit, plot]))])
            right_lane_points = np.array([np.flipud(np.transpose(np.vstack([right_fit, plot])))])
            middle_points = np.hstack((left_lane_points, right_lane_points))

            # draw lane onto blank warped
            cv2.fillPoly(colour_warped, np.int32([middle_points]), (0,255,0)) # green
            cv2.polylines(colour_warped, np.int32([left_lane_points]), isClosed=False,
                          color=(255,0,255), thickness=20)
            cv2.polylines(colour_warped, np.int32([right_lane_points]), isClosed=False,
                          color=(0,255,255), thickness=20)

            fill_design = cv2.warpPerspective(colour_warped, self.frame_matrix, (self.width, self.height))
            final_image = cv2.addWeighted(self.original_frame, 1, fill_design, 0.5, 0)
            
        elif lane_design == 'dotted-curve':
            print(Exception(f"Design '{lane_design}' currently unavailable"))
            exit()
            
        return final_image, template, curve_radius, (pixel_left_quadratic, pixel_right_quadratic)
    
    def start_pipeline(self, visualize=False, sample_video=True):
        if sample_video:
            capture = cv2.VideoCapture('../samples/lane_detection_sample.mp4')
        
        # update figure (frame by frame)
        def update_figure(_):
            # get & make copy of frame(s)
            if sample_video:
                ret, self.original_frame = capture.read()
            else:
                self.original_frame = np.load('../storage/current_frame.pickle', allow_pickle=True)
            if self.original_frame.shape != (self.height, self.width):
                self.original_frame = cv2.resize(self.original_frame, (self.width, self.height))
            
            # preprocess image (mask & edge)
            self.preprocessed_frame = self.preprocess(self.original_frame)

            # un-distort image
            self.undistorted_frame = self.un_distort(self.preprocessed_frame)
        
            # warp image (birds-eye)
            self.warp_frame, self.histogram_peaks = self.warp(self.undistorted_frame)
            
            # curve fit (window method)
            self.final_frame, self.worked_frame, self.curvature_value, lane_equations = \
                              self.curve_fit(self.warp_frame, self.histogram_peaks,
                                             show_windows = False)
            pixel_left_quadratic = lane_equations[0]
            pixel_right_quadratic = lane_equations[1]

            # visualize pipeline
            if visualize:
                # clear axis
                axis1.clear()
                axis2.clear()
                axis3.clear()
                axis4.clear()
                
                # BGR -> RGB
                self.original_frame = cv2.cvtColor(self.original_frame, cv2.COLOR_BGR2RGB)
                self.preprocessed_frame = cv2.cvtColor(self.preprocessed_frame, cv2.COLOR_BGR2RGB)
                self.worked_frame = cv2.cvtColor(self.worked_frame, cv2.COLOR_BGR2RGB)
                self.final_frame = cv2.cvtColor(self.final_frame, cv2.COLOR_BGR2RGB)

                # show original frame
                axis1.imshow(self.original_frame)
                axis1.set_title('Original Frame')

                # show preprocessed frame
                axis2.imshow(self.preprocessed_frame, cmap='gray')
                axis2.set_title('Preprocessed Frame')

                # show & graph warp equations
                axis3_plot = np.linspace(0, self.warp_frame.shape[0] - 1, self.warp_frame.shape[0])
                left_fit = pixel_left_quadratic[0] * axis3_plot ** 2 + pixel_left_quadratic[1] \
                               * axis3_plot + pixel_left_quadratic[2]
                right_fit = pixel_right_quadratic[0] * axis3_plot ** 2 + pixel_right_quadratic[1] \
                            * axis3_plot + pixel_right_quadratic[2]
                axis3.imshow(self.worked_frame)
                axis3.plot(left_fit, axis3_plot, color='orange')
                axis3.plot(right_fit, axis3_plot, color='orange')
                axis3.set_title('Curve Fitted Frame')

                # show final frame
                axis4.imshow(self.final_frame)
                axis4.set_title('Final Frame')

        # figure visualization
        if visualize:
            f, (axis1, axis2, axis3, axis4) = plt.subplots(1, 4, figsize=(20,4.5))
            f.canvas.set_window_title('Lane Detection Pipeline')
            f.tight_layout()
            
            live_lane_detection = dynamic_plt(f, update_figure, interval = 1)
            plt.show()
        else:
            start_time = time.time()
            # print only (no visualization)
            while True:
                try:
                    if sample_video:
                        # get & make copy of frame(s)
                        ret, self.original_frame = capture.read()
                    else:
                        self.original_frane = np.load('../storage/current_frame.pickle', allow_pickle=True)
                    if self.original_frame.shape != (self.height, self.width):
                        self.original_frame = cv2.resize(self.original_frame, (self.width, self.height))
                    
                    # preprocess image (mask & edge)
                    self.preprocessed_frame = self.preprocess(self.original_frame)

                    # un-distort image
                    self.undistorted_frame = self.un_distort(self.preprocessed_frame)
                
                    # warp image (birds-eye)
                    self.warp_frame, self.histogram_peaks = self.warp(self.undistorted_frame)
                    
                    # curve fit (window method)
                    self.final_frame, self.worked_frame, self.curvature_value, lane_equations = \
                                      self.curve_fit(self.warp_frame, self.histogram_peaks,
                                                     show_windows = False)
                    pixel_left_quadratic = lane_equations[0]
                    pixel_right_quadratic = lane_equations[1]
                    
                except KeyboardInterrupt:
                    break
            
RuleBased_ARC = RuleBased()
RuleBased_ARC.start_pipeline(visualize = True)
