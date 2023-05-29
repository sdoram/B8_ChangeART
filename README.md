# B8 - ChangeART

## 프로젝트 컨셉

### 팀명 : I들

프로젝트 개요 : 이미지 화풍 변환 사이트는 사용자가 입력한 원본 이미지와 선택한 화풍 이미지를 기반으로 이미지를 변환해주는 웹 애플리케이션입니다.

이 사이트의 주요 목적은 사용자가 자신이 선택한 화풍을 적용한 이미지를 생성할 수 있는 간편하고 직관적인 방법을 제공하는 것입니다.

## 팀원

- [@JINNY-US](https://github.com/JINNY-US)
- [@chanjulee0309](https://github.com/chanjulee0309)
- [@BenCyera](https://github.com/BenCyera)
- [@Bookwhale00](https://github.com/Bookwhale00)
- [@seman_kim](https://github.com/sdoram)

## 규칙

  - 고민이 있을 때 바로 공유하기 
  - 자리 비울 때 한마디 남기고 가기

## 역할배분

  - 이세희 : Users, 이메일인증

  - 이찬주 : 페이지네이션, 페이지 정렬

  - 박영주 : Articles, 좋아요

  - 김경진 : Change(머신러닝)

  - 김세만 : Comment, git, 테스트코드

## 🛠 사용 스킬 

프론트엔드 `Javascript` `HTML` `CSS`

백엔드 `Python 3.8.10` `Django 4.2.1` `djangorestframework 3.14.0` `tensorflow 2.12.0`

## Front-end

https://github.com/sdoram/B8_ChangeART_front

## Back-end

https://github.com/sdoram/B8_ChangeART

## 컨벤션

Git
  - Git-flow 
  - Gitmoji 

백엔드 
  - 클래스 : PascalCase
  - 변수, 함수 : snake_case
  - URl : kebab-case

## 와이어프레임

![image](https://github.com/sdoram/B8_ChangeART/assets/108051577/2d3981d5-40df-41d1-9f73-80828faec64b)


## ERD

![JJLEGhL6YET4CNmGt](https://github.com/sdoram/B8_ChangeART/assets/108051577/04dee1d5-d106-46f7-9c3e-fbb16aff45b3)

## API 

https://www.notion.so/86d61c6848eb432488856636cc347001?v=1c9b65b7aeb64c0093bf390deaf426bb

## 환경 변수 

이 프로젝트를 실행하려면 secrets.json 파일에 다음 환경 변수를 추가해야 합니다.

`SECRET_KEY` : django secrte_key

`EMAIL_HOST_USER` : 발신할 이메일

`EMAIL_HOST_PASSWORD` : 발신할 메일의 비밀번호

`media/after_image` : 이미지 변환 후 저장 폴더 

## 마음에 드는 코드 

이세희 
  ```javascript
  const userFollowingList = document.getElementById('user_following_list')

  response_json.following_list.forEach(user_following => {
    ...

    userFollowingList.insertBefore(user_newCol,userFollowingList.firstChild); 
  ```
 - js에서는 appendChild를 쓰기 때문에 prepend를 사용할 수 없어서 다른 방법을 찾아보았던 것이 기억에 남는다~

이찬주 
```python
paginator = self.pagination_class()
paginated_articles = paginator.paginate_queryset(articles, request)

serializer = HomeSerializer(paginated_articles, many=True)
return paginator.get_paginated_response(serializer.data)
```
  - 페이지네이션과 페이지정렬 기능이 동시에 postman에서 처음 구동 됐을 때 뿌듯했습니다.

박영주 
```python
# 백엔드
images_data = self.context.get("request").FILES
        for image_data in images_data.getlist("image"):
            Images.objects.create(article=article, image=image_data)
        article.save()
```

```javascript
// 프론트엔드
    if (delete_images.length > 0) {
        formdata.append('delete_images', JSON.stringify(delete_images))
    } else {
        formdata.append('delete_images', '[]')
    }
```
  - 이미지 수정 시 사용자의 선택지를 늘리고 싶었는데(기존 이미지 삭제) 구현할 수 있어서 좋았고 많이 배웠습니다.

김경진 
```javascript
axios({
        url: `${backend_base_url}${get_response_json.after_image}`,
        method: 'GET',
        responseType: 'blob'
    })
        .then((response) => {
            const url = window.URL
                .createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            var name = `${get_response_json.after_image}`.split('_')[1]
            link.setAttribute('download', name);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        })
```
  - 파일을 저장하는 코드가 생각보다 어려웠지만 오류를 차근차근 해결하면서 구현을 한 게 뿌듯해서 기억에 남습니다.

김세만 
```python
            # return에서 instance.id로 js에서 변환된 이미지를 찾을 수 있도록 데이터 보내기
            return Response(serializer.instance.id, status=status.HTTP_201_CREATED)
```
```javascript
    const response_json = await response.json() // post의 return값에서 변환한 이미지의 id 가져오기 
    const get_response = await fetch(`${backend_base_url}/change/${response_json}`, {
    }) // 변환한 이미지의 id를 이용해서 ChangePostView에 get요청
    const get_response_json = await get_response.json() // get요청에서 변환된 이미지 가져오기 
    console.log(get_response_json)
    const after_image = document.getElementById("after_image")
    after_image.setAttribute("src", `${backend_base_url}${get_response_json.after_image}`) // after_image html에 붙여넣기 
```
  - 이 코드를 보면서 백엔드와 프론트가 통신하는 방법을 좀 더 이해할 수 있었습니다. 

