
Buffer<float> pointBuffer : register(t0);

RWTexture2D<uint4> texture : register(u0);
RWTexture2D<uint4> depthmap;

[numthreads(8, 8, 1)]
void main(int3 gid : SV_GroupID, int3 bid : SV_GroupThreadID, int3 tid : SV_DispatchThreadID) {

    float p1,p2;

    p1 = pointBuffer.Load(0);
    p2 = pointBuffer.Load(1);

    float2 p = {p1,p2};
    float2 pos = tid.xy * 250.0;
    float2 z = {(float)tid.x,(float)tid.y};

    float dist = distance(z,p);
    uint4 color = texture[tid.xy];

    if (dist < 40.0) {
        color.r = 0;
        color.b = 255;
        color.g = 0;
        color.a = 255;
    } else {
        color.r = dist-40;
        color.b = 40+255-dist;
        color.g = 0;
        color.a = 255;
    }

    texture[tid.xy] = color;
}