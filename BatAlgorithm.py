import numpy as np
import math

np.random.seed(100)

class BatAlgorithm():
    def __init__(self, dimensi, n_bat, n_generasi, r0, alpha, gamma, fmin, fmax, b_bawah, b_atas, fungsi):
        self.dimensi = dimensi
        self.n_bat = n_bat
        self.n_generasi = n_generasi
        self.alpha = alpha
        self.gamma = gamma
        self.fmin = fmin
        self.fmax = fmax
        self.b_bawah = b_bawah
        self.b_atas = b_atas
        self.fungsi = fungsi
        self.epsilon = 0.001
        self.r0 = r0
        
        #inisialisasi nilai loudness (A) dan pulse rate (r)
        self.A = [0.95 for i in range(self.n_bat)]
        self.r = [self.r0 for i in range(self.n_bat)]
        
        #inisialisasi upperbound dan lowerbound setiap bat
        self.upbound = [[0.0 for i in range(self.dimensi)] for j in range(self.n_bat)]
        self.lowbound =  [[0.0 for i in range(self.dimensi)] for j in range(self.n_bat)]
        
        #inisialisasi nilai 0 untuk semua bat
        self.frekuensi = [0.0] * n_bat
        
        #inisialisasi nilai v (velocity) untuk semua bat
        self.v = [[0.0 for i in range(self.dimensi)] for j in range(self.n_bat)]
        
        #inisialisasi nilai x (lokasi/solusi) untuk semua bat
        self.x = [[0.0 for i in range(self.dimensi)] for j in range(self.n_bat)]
        
        #inisialisasi nilai fitness untuk semua bat
        self.nilai_fitness = [0.0] * n_bat
        self.nilai_fitness_minimum = 0.0
        
        #inisialisasi solusi terbaik
        self.terbaik = [0.0] * dimensi
    
    def bat_terbaik(self):
        i = 0
        j = 0
        #cari nilai fitness terbaik dan catat indeksnya pada variabel j
        for i in range(self.n_bat):
            if self.nilai_fitness[i] < self.nilai_fitness[j] :
                j = i
                
        #simpan nilai-nilai dari setiap dimensi pada solusi terbaik
        for i in range(self.dimensi):
            self.terbaik[i] = self.x[j][i]
        
        #simpan nilai fitness dari solusi terbaik
        self.nilai_fitness_minimum = self.nilai_fitness[j]
    
    def proses_init(self):
        #set semua upperbound dan lowerbound dengan parameter yang telah diset sebelumnya
        for i in range(self.n_bat):
            for j in range(self.dimensi):
                self.lowbound[i][j] = self.b_bawah
                self.upbound[i][j] = self.b_atas
        
        #generate solusi baru dari lowerbound dan upperbound serta set frekuensi semua bat ke 0
        #bat belum mencari target v = 0.
        for i in range(self.n_bat):
            self.frekuensi[i] = 0
            for j in range(self.dimensi):
                random = np.random.uniform(0,1)
                self.v[i][j] = 0.0
                self.x[i][j] = self.lowbound[i][j] + (self.upbound[i][j] - self.lowbound[i][j])*random
            self.nilai_fitness[i] = self.fungsi(self.x[i])
        
        #cari bat dengan nilai fitness terendah (minimum)
        self.bat_terbaik()
    
    def normalisasi_batas(self, nilai):
        #jika nilai melebihi batas atas maka set nilai menjadi batas atas
        if(nilai > self.b_atas):
            nilai = self.b_atas
            
        #jika nilai lebih kecil dari batas bawah maka set nilai menjadi batas bawah
        if(nilai < self.b_bawah):
            nilai = self.b_bawah
        
        return nilai
    
    def proses_ba(self):
        #matriks solusi (banyak bat x dimensi)
        solusi = [[0.0 for i in range(self.dimensi)] for j in range(self.n_bat)]
        
        self.proses_init()
        print(self.nilai_fitness)
        
        for n in range(self.n_generasi):
            Arata2 = np.mean(self.A)
            for i in range(self.n_bat):
                random = np.random.uniform(0,1)
                #cari frekuensi setiap bat dengan menggunakan eq. 2 dari bat algorithm
                self.frekuensi[i] = self.fmin + (self.fmax-self.fmin)*random
                for j in range(self.dimensi):
                    #cari v dan x baru dari setiap bat dengan menggunakan eq. 3 dan 4 dari bat algorithm
                    self.v[i][j] = self.v[i][j] + (self.x[i][j] - self.terbaik[j])*self.frekuensi[i]
                    solusi[i][j] = self.x[i][j] + self.v[i][j]
                    solusi[i][j] = self.normalisasi_batas(solusi[i][j])
                
                random = np.random.uniform(0,1)
                #jika nilai random [0,1] lebih besar dari nilai pulse rate dari bat tersebut, maka lakukan local search berdasarkan bat terbaik
                if(random > self.r[i]):
                    for j in range(self.dimensi):
                        random = np.random.uniform(-1.0,1.0)
                        solusi[i][j] = self.terbaik[j] + random*Arata2
                        solusi[i][j] = self.normalisasi_batas(solusi[i][j])
                
                
                #hitung nilai fitness dari solusi baru
                nilai_fitness = self.fungsi(solusi[i])
                
                random = np.random.uniform(0,1)
                
                if(random < self.A[i] and nilai_fitness < self.nilai_fitness[i]):
                    self.nilai_fitness[i] = nilai_fitness
                    for j in range(self.dimensi):
                        self.x[i][j] = solusi[i][j]
                
                if(self.nilai_fitness[i] < self.nilai_fitness_minimum):
                    #ganti solusi terbaik
                    self.nilai_fitness_minimum = self.fungsi(solusi[i])
                    for j in range(self.dimensi):
                        self.terbaik[j] = self.x[i][j] 
                    
                    #update nilai loudness dan pulse rate setiap bat
                    self.A[i] = self.A[i]*self.alpha
                    self.r[i] = self.r0*(1 - math.exp(-1*self.gamma*i))
            print("Nilai fitness generasi ke (",n,") : ",self.nilai_fitness)
            print("Nilai fitness terbaik ",self.nilai_fitness_minimum)
            print("Solusi terbaik ",self.terbaik)
        print(self.nilai_fitness_minimum)
        print(self.terbaik)
        