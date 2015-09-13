#include <math.h>
#include <stdlib.h>
#include <stdio.h>

double *xyz2lab(double arr[]) {
	double ref_x = 95.047;
	double ref_y = 100.000;
	double ref_z = 108.883;

	arr[0] /= ref_x; arr[1] /= ref_y; arr[2] /= ref_z;

	for (int n = 0; n < 3; n++) {
		if (arr[n] > 0.008856)
			arr[n] = cbrtl(arr[n]);
		else
			arr[n] = (7.787 * arr[n]) + (16 / 116.0);
	}

	double *lab = malloc(3 * sizeof(double));
	lab[0] = (116.0 * arr[1]) - 16;
	lab[1] = 500.0 * (arr[0] - arr[1]);
	lab[2] = 200.0 * (arr[1] - arr[2]);

	return lab;
}

double *rgb2xyz(double arr[]) {
	for (int n = 0; n < 3; n++) {
		if (arr[n] > 0.04045)
			arr[n] = pow((arr[n] + 0.055) / 1.055, 2.4);
		else
			arr[n] /= 12.92;
	}

	for (int n = 0; n < 3; n++) {
		arr[n] *= 100;
	}

	double *xyz = malloc(3 * sizeof(double));
	xyz[0] = arr[0] * 0.4124 + arr[1] * 0.3576 + arr[2] * 0.1805;
	xyz[1] = arr[0] * 0.2126 + arr[1] * 0.7152 + arr[2] * 0.0722;
	xyz[2] = arr[0] * 0.0193 + arr[1] * 0.1192 + arr[2] * 0.9505;

	return xyz;
}

double *rgb2lab(double arr[]) {
	double *xyz = rgb2xyz(arr);
	double *lab = xyz2lab(xyz);
	free(xyz);
	return lab;
}

double edistance(double lab1[], double lab2[]) {
	return sqrt(pow(lab2[0] - lab1[0], 2) + pow(lab2[1] - lab1[1], 2) + pow(lab2[2] - lab1[2], 2));
}

double rgbdiff(double rgb1[], double rgb2[]) {
	double *lab1 = rgb2lab(rgb1);
	double *lab2 = rgb2lab(rgb2);
	double e = edistance(lab1, lab2);
	free(lab1);
	free(lab2);
	return e;
}

double rgbdiff_p(double rgb1_r, double rgb1_g,double rgb1_b,
				double rgb2_r, double rgb2_g, double rgb2_b) {
	double rgb1[3] = {rgb1_r, rgb1_g, rgb1_b};
	double rgb2[3] = {rgb2_r, rgb2_g, rgb2_b};
	return rgbdiff(rgb1, rgb2);
}
