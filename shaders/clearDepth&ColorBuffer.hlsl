
RWTexture2D<uint4> texture : register(u0);
RWTexture2D<float> depthmap : register(u1);

#define FL_MAX 3.402823466e+38F

[numthreads(8, 8, 1)]
void main(int3 tid : SV_DispatchThreadID) {
    texture[tid.xy] = uint4(0,0,0,0);
    depthmap[tid.xy] = FL_MAX;
}