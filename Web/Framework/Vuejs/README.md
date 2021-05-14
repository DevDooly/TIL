## Basic Usage ##

<code>v-model</code> 디렉티브를 사용하여 폼 input과 textarea 엘리먼트에 양방향 데이터 바인딩을 생성할 수 있습니다. 입력 유형에 따라 엘리먼트를 업데이트 하는 올바른 방법을 자동으로 선택합니다. 약간 이상하지만 <code>v-model</code> 은 기본적으로 사용자 입력 이벤트에 대한 데이터를 업데이트하는 <code>syntax sugar</code> 이며 일부 경우에 특별한 주의를 해야합니다.

<pre>`v-model` 은 모든 form 엘리먼트의 초기 `value`와 `checked` 그리고 `selected` 속성을 무시합니다. 항상 Vue 인스턴스 데이터를 원본 소스로 취급합니다. 컴포넌트의 `data` 옵션 안에 있는 JavaScript에서 초기값을 선언해야합니다.</pre>


<code>v-model</code> 은 내부적으로 서로 다른 속성을 사용하고 서로 다른 입력요소에 대해 서로 다른 이벤트를 전송합니다
* text 와 textarea 태그는 <code>value</code> 속성과 <code>input</code> 이벤트를 사용합니다.
* 체크박스들과 라디오버튼들은 <code>checked</code> 속성과 <code>change</code> 이벤트를 사용합니다.
* Select 태그는 <code>value</code> 를 prop으로, <code>change</code> 를 이벤트로 사용합니다.

 [IME](https://ko.wikipedia.org/wiki/입력기)(중국어, 일본어, 한국어 등)가 필요한 언어의 경우 IME 중 `v-model`이 업데이트 되지 않습니다. 이러한 업데이트를 처리하려면 `input` 이벤트를 대신 사용하십시오.

### 연관된 ###
* vuejs-watch

### Reference ###
* [Vue.js 폼 입력 바인딩](https://kr.vuejs.org/v2/guide/forms.html#%EA%B0%92-%EB%B0%94%EC%9D%B8%EB%94%A9%ED%95%98%EA%B8%B0)

## Library ##
* vue-router
* vue-cli
* vuex
* vuetify
* vue-loader
* vue-property-decorator

## Test Tools ##
* Jest
* Cypress

## Style ##
* ESLint
* Prettier
* StyleGuide

## Plugins ##
* rxjs

## Category ##
* TypeScript

## Reference ##
* https://vuejs.org/
* https://vuejs-kr.github.io/
* https://kr.vuejs.org/v2/style-guide/index.html#%EC%9A%B0%EC%84%A0%EC%88%9C%EC%9C%84-B-%EA%B7%9C%EC%B9%99-%EB%A7%A4%EC%9A%B0-%EC%B6%94%EC%B2%9C%ED%95%A8-%EA%B0%80%EB%8F%85%EC%84%B1-%ED%96%A5%EC%83%81%EC%9D%84-%EC%9C%84%ED%95%A8
