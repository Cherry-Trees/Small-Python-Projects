/**
*  Somewhat calculates sin(x) using only basic integer addition and subtraction
*/
public class Calculator {

	public static void main(String[] args) {
		
		// (227, 2) -> 227*10^-2 = 2.27
		System.out.println("sin(2.27) = "+sin(227, 2));
	}
		
	static int abs(int x) {
		if (x<0) {return -x;}
		else {return x;}
	}
	
	static int mod(int a, int b) {
		while (a >= b) {a = a - b;}
		return a;
	}
	
	static int digits(int n) {
		n = abs(n);
		int digits = 0;
		while (n!=0) {
			n = div_even(n, 10);
			digits++;
		}
		return digits;
	}
	
	static int round(int x, int to) {
		int x_abs = abs(x);
		if (to <= digits(x_abs)) {
			int new_x = div_even(x_abs, pow(10, digits(x_abs)-to));
			if (mod(x_abs, pow(10, digits(x_abs)-to)) >= multiply(5, pow(10, digits(x_abs)-to-1))) {
				new_x = (x<0) ? new_x-1 : new_x+1;
			}
			return (x<0) ? -new_x : new_x;
		}
		else {
			x_abs = multiply(x_abs, pow(10, to-digits(x_abs)));
			return (x<0) ? -x_abs : x_abs;
		}
	}
	
	static int multiply(int a, int b) {
		if (a==0 || b==0) {return 0;}
		else {
			int sum = 0;
			int min = (a <= b) ? a : b;
			int max = (a > b) ? a : b;
			for (int i=0; i<abs(min); i++) {
				sum = sum + abs(max);
			}
			if ((a<0 && b<0) || (a>0 && b>0)) {return sum;}
			else {return -sum;}
		}
	}
	
	static int[] multiply(int a, int a_exp, int b, int b_exp) {
		if (a==0 || b==0) {
			int[] arr = {0, a_exp + b_exp};
			return arr;
		}
		else {
			int sum = 0;
			int min = (a <= b) ? a : b;
			int max = (a > b) ? a : b;
			for (int i=0; i<abs(min); i++) {
				sum = sum + abs(max);
			}
			if ((a<0 && b<0) || (a>0 && b>0)) {}
			else {sum = -sum;}
			int[] arr = {sum, a_exp + b_exp};
			return arr;
		}
	}
	
	static int pow(int x, int pow) {
		if (pow == 0) {return 1;}
		else {
			int sum = 0;
			int abs_x = abs(x);
			int temp = abs_x;
			for (int i=0; i<pow-1; i++) {
				for (int j=0; j<abs_x; j++) {
					sum = sum + temp;
				}
				temp = sum;
				sum = 0;
			}
			if (x<0 && mod(pow, 2)==1) {return -temp;}
			else {return temp;}
		}
	}
	
	static int[] pow(int x, int x_exp, int pow) {
		if (pow == 0) {
			int[] arr = {1, 0};
			return arr;
		}
		else {
			int sum = 0;
			int temp = x;
			for (int i=0; i<pow-1; i++) {
				for (int j=0; j<x; j++) {
					sum = sum + temp;
				}
				temp = sum;
				sum = 0;
			}
			int[] arr = {temp, multiply(x_exp, pow)};
			return arr;
		}
	}
	
	static int div(int a, int b) {
		int temp = a;
		int sum = 0;
		int count = 0;
		for (int i=7; i>0; i--) {
			while (temp >= b) {
				temp = temp - b;
				count++;
			}
			temp = multiply(temp, 10);
			sum = sum + multiply(count, pow(10, i-1));
			count = 0;
			if (temp == 0) {break;}
		}
		return sum;
	}
	
	static int[] div(int a, int a_exp, int b, int b_exp) {
		int temp = a;
		int sum = 0;
		int sum_exp = 0;
		int count = 0;
		for (int i=7; i>0; i--) {
			while (temp >= b) {
				temp = temp - b;
				count++;
			}
			temp = multiply(temp, 10);
			sum = sum + multiply(count, pow(10, i-1));
			count = 0;
			sum_exp++;
		}
		int exp = a_exp - b_exp - sum_exp + 1;
		int[] arr = {sum, exp};
		return arr;
	}
	
	static int div_even(int a, int b) {
		int count = 0;
		while (a >= b) {
			a = a - b;
			count++;
		}
		return count;
	}
	
	static int fact(int n) {
		if (n==0) {return 1;}
		else {return multiply(n, fact(n-1));}
	}
	
	static int coterminal(int rad, int rad_exp) {
		final int PI2 = 62832;
		final int EPSILON = (rad_exp<-2) ? 100 : pow(10, 3+rad_exp);
		int rad_ext = multiply(rad, pow(10, 4+rad_exp));
		int temp = rad_ext;
		while (abs(temp - multiply(div_even(temp, pow(10, 4)), pow(10, 4))) > EPSILON) {
			temp = temp + PI2;
		}
		return div_even(temp, pow(10, 4));
	}
	
	static int sin_small(int x) {
		if (digits(x) > 3) {
			return -1;
		}
		else {
			return x;
		}
	}
	
	static int cos_small(int x) {
		if (digits(x) > 3) {
			return -1;
		}
		else {
			int x_square = pow(x, -digits(x), 2)[0];
			int x_square_exp = pow(x, 2, -digits(x))[1];
			
			
			while (digits(x_square) > 3) {
				x_square = div_even(x_square, 10);
				x_square_exp++;
			}
			
			int half = div(x_square, x_square_exp, 2, 0)[0];
			int half_exp = div(x_square, x_square_exp, 2, 0)[1];
			while (mod(half, 10) == 0) {
				half = div_even(half, 10);
				half_exp++;
			}		
			return pow(10, -half_exp) - half;
		}
	}
		
	static int sin(int x, int x_exp) {
		if (digits(x) < x_exp) {
			return sin_small(x);
		}
		else {
			int x_int = div_even(x, pow(10, abs(x_exp)));
			int x_float = mod(x, pow(10, abs(x_exp)));
	
			int identity_part1 = multiply(round(sin0(x_int), 4), round(cos_small(x_float), 4));
			int identity_part2 = multiply(round(cos0(x_int), 4), round(sin_small(x_float), 4));
			return identity_part1 + identity_part2;
		}
	}
	
	static int sin0(int x) {
		int sum = 0;
		int xn, quot;
		for (int i=0; i<8; i++) {
			xn = pow(abs(x), multiply(2, i)+1);
			quot = div(xn, fact(multiply(2, i)+1));	
			if (mod(i, 2) == 0) {sum = sum + quot;}
			else {sum = sum - quot;}
		}
		return (x<0) ? -sum : sum;
	}
	
	static int sin22(int x) {
		int sum = 0;
		int xn, quot;
		for (int i=0; i<8; i++) {
			xn = pow(abs(x-22), multiply(2, i)+1);
			quot = div(xn, fact(multiply(2, i)+1));	
			if (mod(i, 2) == 1) {sum = sum + quot;}
			else {sum = sum - quot;}
		}
		return (x<22) ? -sum : sum;
	}
	
	static int cos0(int x) {
		int sum = 0;
		int xn, quot;
		for (int i=0; i<8; i++) {
			xn = pow(x, multiply(2, i));
			quot = div(xn, fact(multiply(2, i)));	
			if (mod(i, 2) == 0) {sum = sum + quot;}
			else {sum = sum - quot;}
		}
		return sum;
	}
	
	static int exp(int x) {
		int sum = 0;
		int xn, quot;
		for (int i=0; i<17; i++) {
			xn = pow(x, i);
			quot = div(xn, fact(i));	
			sum = sum + quot;
		}
		return sum;
	}
	
}
