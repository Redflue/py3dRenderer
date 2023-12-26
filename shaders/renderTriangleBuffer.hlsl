
Buffer<float> pointBuffer : register(t0);
Buffer<uint> colorBuffer : register(t1);

RWTexture2D<uint4> texture : register(u0);
RWTexture2D<float> depthmap : register(u1);

#define FL_MAX 3.402823466e+38F

bool areValuesInTriangle(float3 values) {
    return (values.x >= 0.0 && values.y >= 0 && values.x+values.y <= 1);
}

float3 getTriangleValues(float3 a, float3 b, float3 c, float2 p) {
    float w1 = (a.x*(c.y-a.y)+(p.y-a.y)*(c.x-a.x)-p.x*(c.y-a.y))/((b.y-a.y)*(c.x-a.x)-(b.x-a.x)*(c.y-a.y));
    float w2 = (p.y-a.y-w1*(b.y-a.y))/(c.y-a.y);
    float w3 = 1-(w1+w2);
    return float3(w1,w2,w3);
}

[numthreads(8, 8, 1)]
void main(int3 gid : SV_GroupID, int3 bid : SV_GroupThreadID, int3 tid : SV_DispatchThreadID) {

    float2 p = float2(tid.x, tid.y);
    uint amount; pointBuffer.GetDimensions(amount); amount = amount/9;
    for (int i = 0; i < amount; i++) {
        float3 p1 = float3(pointBuffer.Load(i*9 + 0), pointBuffer.Load(i*9 + 1), pointBuffer.Load(i*9 + 2));
        float3 p2 = float3(pointBuffer.Load(i*9 + 3), pointBuffer.Load(i*9 + 4), pointBuffer.Load(i*9 + 5));
        float3 p3 = float3(pointBuffer.Load(i*9 + 6), pointBuffer.Load(i*9 + 7), pointBuffer.Load(i*9 + 8));

        uint4 triColor;
        triColor.r = colorBuffer.Load((i*4)+0);
        triColor.g = colorBuffer.Load((i*4)+1);
        triColor.b = colorBuffer.Load((i*4)+2);
        triColor.a = 255;

        float3 vals = getTriangleValues(p1,p2,p3,p);

        if (areValuesInTriangle(vals)) {
            
            float oldDepth = depthmap[tid.xy];
            float curDepth = (vals.x*p2.z+vals.y*p3.z+vals.z*p1.z)/3;

            uint4 col;
            col.a = 255;
            col.r = vals.x*255;
            col.g = vals.y*255;
            col.b = vals.z*255;
            // col.rgb = 255-curDepth*50;

            triColor.rbg += clamp(curDepth*25,0,255);
            
            if (curDepth < oldDepth && curDepth >= 0.1) {
            // if (curDepth < oldDepth && curDepth >= 0 && curDepth*50 < 255) {
                texture[tid.xy] = triColor;
                // texture[tid.xy] = col;
                depthmap[tid.xy] = curDepth;
            }
        }
    }
}