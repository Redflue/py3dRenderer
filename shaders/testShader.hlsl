
RWTexture2D<uint4> texture : register(u0);

[numthreads(2, 2, 1)]
void main(int3 tid : SV_DispatchThreadID) {
    uint4 color = texture[tid.xy];
    color.r = 255;
    color.a = 255;
    texture[tid.xy] = color;
}