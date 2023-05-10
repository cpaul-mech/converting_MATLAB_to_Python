# This function will match with this matlab code
"""function ydot = odefun1(t,y)
% QUESTION 4

%PART 3!!!
ydot = (-0.002767227166952 * y)/.0264 ;

end"""

def ode_fun1(t,y):
    ydot = (-0.002767227166952 * y)/.0264
    return ydot