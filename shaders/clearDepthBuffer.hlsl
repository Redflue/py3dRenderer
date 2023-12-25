
RWTexture2D<float> depthmap : register(u0);

#define FL_MAX 3.402823466e+38F

[numthreads(8, 8, 1)]
void main(int3 tid : SV_DispatchThreadID) {
    depthmap[tid.xy] = FL_MAX;
}