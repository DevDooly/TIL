# Single Quotation vs Double Quotation in bash #
## Single Quotation ##
작은 따옴표 (<code> ' </code>) 안에 있는 각 문자의 리터럴 값을 유지합니다. 백 슬래시가 앞에있는 경우에도 작은 따옴표 사이에 작은 따옴표를 사용할 수 없습니다.

출처 : http://www.gnu.org/software/bash/manual/html_node/Single-Quotes.html

## Double Quotation ##
큰 따옴표 (<code> " </code>) 는 <code>'</code> 를 제외하고 따옴표 안에있는 모든 문자의 리터럴 값을 유지합니다. $','`','\', 히스토리 확장이 활성화되면'!'. 쉘이 POSIX 모드 ( Bash POSIX 모드 참조 )에있을 때 '!'는 히스토리 확장이 활성화 된 경우에도 큰 따옴표 안에 특별한 의미가 없습니다. 문자 <code> $ </code> 및 <code> ` </code> 는 큰 따옴표 안에 특별한 의미를 유지합니다 ( 셸 확장 참조 ). 백 슬래시는 다음 문자 중 하나가 뒤에 오는 경우에만 특별한 의미를 유지합니다. '$','`','"','\'또는 newline. 큰 따옴표 내에서 이러한 문자 중 하나가 뒤에 오는 백 슬래시가 제거됩니다. 특별한 의미가없는 문자 앞의 백 슬래시는 수정되지 않은 상태로 남습니다. 큰 따옴표 앞에 백 슬래시를 붙여 큰 따옴표로 묶을 수 있습니다. 활성화하면 '!'큰 따옴표로 묶인 경우 백 슬래시를 사용하여 이스케이프됩니다. '앞의 백 슬래시!'이 제거되지 않았습니다.

특수 매개 변수 <code> * </code> 및 <code> @ </code> 는 큰 따옴표 안에있을 때 특별한 의미가 있습니다 ( 쉘 매개 변수 확장 참조 ).

출처 : http://www.gnu.org/software/bash/manual/html_node/Double-Quotes.html
