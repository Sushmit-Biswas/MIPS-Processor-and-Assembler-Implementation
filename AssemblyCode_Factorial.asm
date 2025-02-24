main:
	
	addi $t0, $0, 10                       #t0 = n = 10
	addi $t1, $0, 268500992                #t1 = memory address where n will be stored    
	sw $t0, 0($t1)                         #M[t1] = t0 = 10
	lw $s0, 0($t1)                         #s0 = M[t1] = n = 10
	addi $s1, $0, 1                        #s1 = i = 1
	addi $s2, $0, 1                        #s2 = fact(n) =  1
	j check

check:          #checks the loop condition

	bne $s1, $s0, loop             #if (i!=n) jump to loop
	mul $s2, $s2, $s0              #else fact = fact * n because the loop function will execute only till (n-1)
	j exit
	
loop:
	mul $s2, $s2, $s1              # fact = fact * i       
	addi $s1, $s1, 1               # i = i+1
	j check
	
exit:
	addi $t0, $0, 268501024        #t0 = address where the result will be stored
        sw $s2, 0($t0)                 #M[t0] = s2
        addi $v0,$0,10                 # return 0
        syscall
