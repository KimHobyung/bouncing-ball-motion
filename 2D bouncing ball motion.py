# 이 프로그램은 회전하는 공의 튕김 운동에 대한 시뮬레이션이다.
# 사용된 물리량은 모두 SI 단위계를 따른다. 즉, 시간은 sec, 길이는 miter, 질량은 kg 단위이다.
# 초기 조건에 따라 공은 에너지를 잃으며 +x 방향으로 순행할 수도 있고, -방향으로 역행할 수도 있다.

import numpy as np
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt

# 초기 조건
left_wall, right_wall = -20, 20
x_i, y_i = 0, 10 # 초기 위치
v_xi, v_yi =  15, 20 # 초기 속도
w_i = 10 # 초기 각속도
m = 1 # 질량
R = 5 # 반지름
e = 0.7 # 반발 계수
mu = 0.3 # 마찰 계수
g = 9.8 # 중력 가속도
c = 0.4 # 공의 회전관성 상수
I = c*m*R**2 # 공의 회전관성

# 초기 에너지
E = 0.5*m*(v_xi**2 + v_yi**2) + m*g*y_i + 0.5*I*w_i**2
count = 0 # 튕긴 횟수
x_count = 0

# 실시간으로 변하는 물리량
x, y = x_i, y_i # 위치
v_x, v_y = v_xi, v_yi # 속도
w = w_i # 각속도
dt = 0.01 # 시간 간격

# 모션이 복잡하여 시간에 따라 점점 투명해지는 그래프가 필요함
segments = []
colors = []


position_x = [] # 시간 간격에 대한 공의 x 위치
position_y = [] # 시간 간격에 대한 공의 y 위치

v_list = [[v_xi, v_yi]] # 시간 간격에 대한 공의 속도
w_list = [w_i] # 시간 간격에 대한 공의 각속도
E_list = [E] # 튕길 때 마다 총 에너지 기록

x_v_list = [[v_xi, v_yi]]

while E > 0 and count < 15: # 초기 에너지가 0이 될 때 까지 반복한다. 만약 10번 튕겨도 에너지가 0이 아니라면 시뮬레이션 종료

    if y > 0: # 공이 포물선 운동을 하는 상황
        
        if x < right_wall and x > left_wall: # 벽에 닿지 않는 경우
            x = x + v_x*dt
            y = y + v_y*dt
            v_y = v_y - g*dt

            position_x.append(x)
            position_y.append(y)

         


        else: # 벽에 튕기는 경우
            v_xf2 = -e*x_v_list[-1][0]

            if abs(w_list[-1]) > (1/(c*R))*(1+e)*abs(x_v_list[-1][0]):

                w = w_list[-1]+(-1)*(w_list[-1]/abs(w_list[-1]))*(1/(c*R))*(1+e)*(x_v_list[-1][0]/abs(x_v_list[-1][0]))*x_v_list[-1][0]
                w_list.append(w)

                v_yf2 = v_y +(-1)*mu*(1+e)*(x_v_list[-1][0]/abs(x_v_list[-1][0]))*(v_y/abs(v_y))*v_y
            else:
                v_yf2 = v_y
                w = w_list[-1]
                w_list.append(w)
            
            v_x = v_xf2
            v_y = v_yf2

            if x >= right_wall:
                x = right_wall - 0.1
            elif x <= left_wall:
                x = left_wall + 0.1

            v_list.append([v_xf2, (v_yf2/abs(v_yf2+0.01))*(v_yf2**2 + 2*g*y)**0.5])
            x_v_list.append([v_xf2, v_yf2])

            E = E - 0.5*(1-e**2)*e**(2*x_count) - R*0.5*(abs(w_list[-1]+w_list[-2]))*m*mu*(1+e)*e**(x_count)*abs(x_v_list[-1][0])
            E_list.append(E)

    else: # y = 0이 되어 공이 바닥과 충돌하여 튕기는 상황

        if count == 0: # 만약 처음 튕기는 상황이라면 (처음 튕길 때와 나중에 튕길 때 적용되는 식에 약간의 차이가 있음)
       
            if abs(w_list[-1]) > (1/(c*R))*mu*(1+e)*(v_list[-1][1]**2 + 2*g*y_i)**0.5:
                v_xf = v_list[-1][0] +(v_list[-1][0]/(abs(v_list[-1][0])))*((1/(c*R))-1*((w_list[-1]/abs(w_list[-1]))*(v_list[-1][0]/(abs(v_list[-1][0])))))*mu*(1+e)*(v_list[-1][1]**2 + 2*g*y_i)**0.5
            else:
                v_xf = v_list[-1][0] - (v_list[-1][0]/(abs(v_list[-1][0])))*mu*(1+e)*(v_list[-1][1]**2 + 2*g*y_i)**0.5
            
            v_yf = e*(v_list[-1][1]**2 + 2*g*y_i)**0.5
            v_list.append([v_xf, v_yf]) # 튕긴 후 새로운 초기속도를 부여받음

            v_x = v_xf
            v_y = v_yf
            y = 0.1 # 공을 다시 0.1m 높이에서 발사

            if abs(w_list[-1]) > (1/(c*R))*mu*(1+e)*(v_list[-1][1]**2 + 2*g*y_i)**0.5:
                w = w_list[-1] +(-1)*(w_list[-1]/abs(w_list[-1]))*(1/(c*R))*mu*(1+e)*(v_list[-1][1]**2 + 2*g*y_i)**0.5
            else:
                w = w_list[-1]
            w_list.append(w) # 각속도 리스트에 기록

            E = E - m*g*y_i*(1-e**2)*e**(2*count) - R*0.5*(abs(w_list[-1]+w_list[-2]))*m*mu*(1+e)*(v_yi**2 + 2*g*y_i)**0.5 # 충돌 후 감소한 에너지
            count += 1
            E_list.append(E) # 에너지 리스트에 기록
            
        else: # 두번째 이후로 튕길 때

            if abs(w_list[-1]) > (1/(c*R))*mu*(1+e)*v_list[-1][1]:
                v_xf = v_list[-1][0] +(v_list[-1][0]/(abs(v_list[-1][0])))*((1/(c*R))-1*((w_list[-1]/abs(w_list[-1]))*(v_list[-1][0]/(abs(v_list[-1][0])))))*mu*(1+e)*v_list[-1][1]
            else:
                v_xf = v_list[-1][0] - (v_list[-1][0]/(abs(v_list[-1][0])))*mu*(1+e)*v_list[-1][1]

            v_yf = e*v_list[-1][1]
            v_list.append([v_xf, v_yf])

            v_x = v_xf
            v_y = v_yf
            y = 0.1

            if abs(w_list[-1]) > (1/(c*R))*mu*(1+e)*(v_list[-1][1]**2 + 2*g*y_i)**0.5:
                w = w_list[-1] +(-1)*(w_list[-1]/abs(w_list[-1]))*(1/(c*R))*mu*(1+e)*v_list[-1][1]
            else:
                w = w_list[-1]
            w_list.append(w) # 각속도 리스트에 기록

            E = E - m*g*y_i*(1-e**2)*e**(2*count) - R*0.5*(abs(w_list[-1]+w_list[-2]))*m*mu*(1+e)*abs(v_list[-1][1])
            count += 1
            E_list.append(E)

# 모션이 복잡하여 시간에 따라 점점 투명해지는 그래프가 필요함
segments = []
colors = []


for i in range(len(position_x) - 1):
    segment = [(position_x[i], position_y[i]), (position_x[i+1], position_y[i+1])]
    segments.append(segment)
    alpha = (1 - i) / (len(position_x) - 1)  # 색상 투명도
    colors.append((0, 0, 1, alpha))  # RGB 값 + alpha

# 튕김 후 변화된 물리량 확인하기 

print("벽에 튕긴 v: ", x_v_list)
print("w: " , w_list)
print('E: ', E_list)
# print('v: ', v_list)


# LineCollection 생성
lc = LineCollection(segments, colors=colors, linewidth=2)

# 플롯 설정
fig, ax = plt.subplots()
ax.add_collection(lc)
ax.autoscale()
ax.set_xlim(np.min(position_x), np.max(position_x))
ax.set_ylim(np.min(position_y), np.max(position_y)+5)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('xy bouncing motion')

plt.show()
