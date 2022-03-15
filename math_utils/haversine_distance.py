import math

def compute(latitude_1,longitude_1,latitude_2,longitude_2,radius):
    phi_1 = math.radians(latitude_1)
    phi_2 = math.radians(latitude_2)
    lambda_1 = math.radians(longitude_1)
    lambda_2 = math.radians(longitude_2)
    sin_half_delta_phi = math.sin((phi_2-phi_1)*0.5)
    sin_half_delta_lambda = math.sin((lambda_2-lambda_1)*0.5)
    cos_latitude_1 = math.cos(phi_1)
    cos_latitude_2 = math.cos(phi_2)
    h =  sin_half_delta_phi**2 + cos_latitude_1*cos_latitude_2*(sin_half_delta_lambda**2)
    return 2*radius*math.asin(math.sqrt(h))


if __name__ == "__main__":
    lyon = (45.7597, 4.8422)
    paris = (48.8567, 2.3508)
    radius = 6378
    print(compute(*lyon,*paris,radius))