#binary search
.data
	arr: .word 11, 20, 34, 45, 56  #sorted array 
.text

addi $s0,$zero,5               #store size of array in $s0
addi $s1,$zero,45              #number to be found 
la $t1,arr                     #store base address of array

addi $t7,$zero,0               #lowerbound=0
addi $t6,$s0,-1                #upperbound=size-1

loop:   bgt $t7,$t6,not_found  #if lowerbound>upperbound, search is over
	add $t5,$t7,$t6        #mid = lb+ub
	srl  $t5,$t5,1         #mid = lb+ub/2
	sll $t4,$t5,2          #mid*4 for alignment
	add $t4,$t4,$t1        #store address of arr[mid]
	lw $t3, 0($t4)         #$t3 = arr[mid] 
	beq $t3,$s1, found     #arr[mid] = key 
	blt $t3,$s1,else       #if arr[mid]<key
	addi $t6,$t5,-1        #ub= mid-1
	j loop
	
else:   addi $t7,$t5,1         #lb=mid+1
	j loop
	
found:  addi $t0,$0,268501024  #t0 = address where the result will be stored
        sw $t5,0($t0)          #M[t0] = t5 = index of element found
        j exit 
        
not_found: 
	addi $t5,$zero,-1      #to store -1 if no. not found
	addi $t0,$0,268501024  #t0 = address where the result will be stored
        sw $t5,0($t0)          #M[t0] = t5 
  
exit:  
	addi $v0,$0,10         #exit program
        syscall
