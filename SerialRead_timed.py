import serial
import time as clk
import matplotlib.pyplot as plt
import cmath as cmat
import math as mat
import numpy as num

def FFT(x):
    N = len(x);
    W_N = [];
    k = mat.floor(mat.log(N)/mat.log(2));
    i_max = num.linspace(0,k,k+1);
    for i in i_max:
        W_N.append((cmat.e**((-((-1)**(1/2))*2*cmat.pi)/N))**i);
    
    print(W_N, i_max[1:]);
    S = [];
    dim = (8,8);
    for i in i_max[1:]:
        S_temp = num.zeros(dim);
        
        dim_sub = int((2**i));
        dim_sub = (dim_sub,dim_sub);
        S_sub = num.zeros(dim_sub);
        
        i_max = num.linspace(0,dim_sub-1,dim_sub);
        unchange = 1;
        for i_row in i_max:
            if(i_row >=  dim_sub/2):
                if(unchange == 1):
                    unchange = 0;
                    S_sub[i_row:][:] = S_sub[:i_row][:];
                    S_sub[i_row:][i_row:] = (-1)*S_sub[:i_row][i_row:]
            else:
                for i_col in i_max:
                      x = 1;
        S.append(S_temp);
    print(S);

def DFT(x,t,flag):
    T = 0;
    N = len(t);
    i_prev = 0;
    for i in t:
        T += (i-i_prev)/N;
        i_prev = i;
    print("delta_t: " + str(T));
    #print(T);
    #print(N);
    X = [];
    X_real = [];
    X_imag = [];
    X_abs = [];
    omega_k = [];
    omega = (2*cmat.pi)/((N)*T)
    print("delta_omega: " + str(omega));
    i = num.linspace(0,(N-1),N);
    print("number of samples: " + str(N));
    time_calc_est = 0;
    time_est_temp = 0;
    timer_temp = 0;
    timer_interval = 0;
    for k in i:
        if (k%100 == 0 and k != 0):
            timer_interval += 1;
            if(timer_interval%2 != 0):
                timer_temp = clk.time();
        
        newX_e = complex(0);
        if k != 0:
            for n in i:
                newX_e += complex(x[int(n)])*cmat.exp( -( ( (-1)**(1/2) )*k*omega*n*T ) );
        X.append(newX_e);
        X_real.append(newX_e.real);
        X_imag.append(newX_e.imag);
        X_abs.append(mat.pow((newX_e.real**2)+(newX_e.imag**2),0.5));
        omega_k.append(omega*k);
        
        
        if (k%100 == 0 and k != 0):
            if(timer_interval%2 == 0):
                timer_temp = clk.time() - timer_temp;
                time_est_temp = (time_est_temp + timer_temp)/(100);
                time_calc_est = time_est_temp*(N-k);
                print("Estimated time left is "+ str(mat.floor(time_calc_est/(60**2))) + " [h]  and  " + str(mat.floor(time_calc_est/60) - mat.floor(time_calc_est/(60**2))*60) + " [m]  and  " + str(mat.floor(time_calc_est) - mat.floor(time_calc_est/60)*60) + " [s]  and  " + str(mat.floor(1000*time_calc_est) - 1000*mat.floor(time_calc_est)) + " [ms]");
    
    """ plotting data
    """
    if (flag == 1):
            
        plt.figure(figsize=(16,8));
        
        plt.subplot(231);
        plt.title('time domain [V(t)]');
        plt.plot(t,x);
        plt.subplot(232);
        plt.title('freq domain [V(Hz)] - abs');
        plt.plot(omega_k,X_abs);
        plt.subplot(233);
        plt.title('fourier transformed dataset');
        plt.scatter(X_real,X_imag);
        plt.subplot(234);
        plt.title('freq domain [V(Hz)] - real');
        plt.plot(omega_k,X_real);
        plt.subplot(235);
        plt.title('freq domain [V(Hz)] - imag');
        plt.plot(omega_k,X_imag);
        plt.show();
    
    """
    plt.figure(figsize=(9, 3))

    plt.subplot(131)
    plt.bar(names, values)
    plt.subplot(132)
    plt.scatter(names, values)
    plt.subplot(133)
    plt.plot(names, values)
    plt.suptitle('Categorical Plotting')
    plt.show()"""
            
    
def myread():
    timerMax = 30
    timeout = clk.time() + timerMax;
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = 'COM7'
    print(ser)
    ser.open()
    print(ser.is_open)
    i=0;
    t = [];
    x = [];
    while(clk.time() < timeout ):
        
        """a = ser.readline();
        a = a[:-2];
        print(a)
        i= i + 1;"""
        n = i;
        buffer = "";
        while i == n:
            oneByte = ser.read(1)
            if oneByte == b"\n":    #method should returns bytes
                #print (buffer)
                timer = timerMax - (timeout - clk.time())
                #print(timer)
                i = i + 1;
            else:
                buffer += oneByte.decode()
        t.append(timer);
        x.append(float(buffer));
    #print(t,x);
    ser.close();
    print("done reading com port ! after " + str(clk.time()-(timeout - timerMax)) + " [s]")
    for i in num.linspace(0,10,11):
        x[int(i)] = x[int(11)];
    DFT(x,t,1)
    

def main():
    ser = serial.Serial(
        port='COM8',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS)
    ser.timeout=5
    ser.write("OUTP? 1 \r\n".encode()) #Asks the Lock-in for x-value
    ser.write("++read\r\n".encode())
    buffer = ""
    while True:
        oneByte = ser.read(1)
        if oneByte == b"\r":    #method should returns bytes
            print (buffer)
            break
        else:
            buffer += oneByte.decode()
def sineSim():
    x =[];
    t = [];
    w = (10**(-3))*2*mat.pi;
    dt = 1;
    N = 37000;
    n = num.linspace(0,N,N+1);
    print(n);
    a = 0;
    for i in n:
        t.append(i*dt);
        x.append(mat.sin(w*t[int(a)]));
        a += 1;
    plt.plot(t,x);
    plt.show();
    DFT(x,t,1);
def test8point():
    x = [0,0,1,1,1,0,0,0];
    dt = 0.1;
    t = [];
    i_max = num.linspace(0,7,8);
    for i in i_max:
        t.append(dt*i);
    DFT(x,t,1);
    FFT(x);
#test8point();
sineSim()           
#myread()
#main()
    
Y = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]];
print(Y[2:][:])
print(Y[:2][:])