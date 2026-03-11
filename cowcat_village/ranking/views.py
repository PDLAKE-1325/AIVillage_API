from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Score
from .serializers import ScoreSerializer

# @api_view(['POST'])
# def submit_score(request):
#     serializer = ScoreSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def submit_score(request):
    username = request.data.get('username')
    score = request.data.get('score')
    
    if not username or score is None:
        return Response(
            {'error': 'username과 score가 필요합니다.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 기존 유저가 있는지 확인
    existing_user = Score.objects.filter(username=username).first()
    
    if existing_user:
        # 기존 점수보다 높으면 업데이트
        if score > existing_user.score:
            existing_user.score = score
            existing_user.save()
            return Response({
                'message': '점수가 갱신되었습니다!',
                'data': ScoreSerializer(existing_user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': '기존 점수가 더 높습니다.',
                'data': ScoreSerializer(existing_user).data
            }, status=status.HTTP_200_OK)
    else:
        # 새로운 유저 추가
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': '새로운 점수가 등록되었습니다!',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_rankings(request):
    top_scores = Score.objects.all()[:3]  # 점수 높은 순으로 3개
    serializer = ScoreSerializer(top_scores, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def clear_scores(request):
    count = Score.objects.all().count()
    Score.objects.all().delete()
    return Response({
        'message': f'{count}개의 점수 데이터가 삭제됨',
        'deleted_count': count
    }, status=status.HTTP_200_OK)