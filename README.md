# Predict_AudienceSize

### 关于京东数坊人数计算API接口的调用

#### Step1 ：插件下载，直接获取cookies

- 导出的txt文件命名为：cookies.txt,存放在根目录中

![1](pic/1.png)


- google的插件我放在cookies_extension文件夹中，googel插件管理，打开开发者模式，然后选择加载已解压的扩展程序，

![6](pic/6.png)

> 为了减少F12查找类目Id的繁琐步骤，已经将JDCategory.json中JD的全类目名和类目ID的全部信息，解析JDCategory.json的代码在sub_code文件夹中的category_build.py，感兴趣可以交流学习，类似下图：

>![5](pic/5.png) <br>
>可以将此表与date_sheet.xlsx的类目ID结合，每次只需要填写类目名称，通过vlookup直接匹配过来


#### Step2： 根据相关业务填写data_sheet.xlsx表
![2](pic/2.png)

1.其中**人群名称、运算规则、卡片名称**为必填单元格<br>

2.同一个人群包（不得超过30个卡片）的`人群名称`需保持一致，命名规则根据个人命名偏好修改，无影响；<br>

3.若人群包中只有一个卡片，运算规则需填写“空”字，或者不填写，但是**交集、并集、差集不可省略**；<br>

4.对于有频次、价格、sku、关键词等限制条件的，逗号需使用英文模式下的逗号，中文模式下的识别可能会出现报错<br>

5.关于价格，所有维度的价格均为成交价，非京东价<br>

6.如有其他特定维度的批量取数需求，可以交流，我再添加~

7.4A只能支持品牌维度的人群计算，使用场景不高，暂未添加相关方法。

**目前支持的维度（持续更新中……）**
- 浏览行为_品牌/类目
> **`get_view_data(brand_id, cate_id, start_time, end_time, frequency, price)`**<br>
> 固定维度为品牌x三级类目、品牌、三级类目维度，根据需求在data_sheet中填写相关的数据
- 浏览行为_店铺
>**`get_view_shop_data(shop_id,start_time, end_time, frequency, price)`**<br>
>固定维度为店铺内商品维度，此时的Key_ID不是写品牌ID，而是店铺ID
- 购买行为_品牌/类目
> **`get_order_data(brand_id, cate_id, start_time, end_time, frequency, price)`**<br>
> 固定维度为品牌x三级类目、品牌、三级类目维度，根据需求在data_sheet中填写相关的数据
- 购买行为_店铺
>**`get_order_shop_data(shop_id,start_time, end_time, frequency, price)`**<br>
>固定维度为店铺内商品维度，此时的Key_ID不是写品牌ID，而是店铺ID
- 购买行为_关键词x三级类目
> **`get_order_keycate_data(shop_id,cate_id,keyWords,start_time, end_time, frequency, price)`**<br>
>固定维度为关键词x三级类目，此时的Key_ID不填写，需填写KeyWords（关键词）和类目
- 购买行为_SKU
> **`get_order_sku_data(sku_list,start_time, end_time, frequency, price)`**<br>
>固定维度为SKU维度，其中SKU上限是100个，SKU输入到data_sheet的`sku_list`中
- 已有人群
>**`get_old_data(id_list,name)`**
> 已有人群除必填信息外，其他信息信息无需填写，只需要讲已有人群包的人群包名称填写到`已有人群`列
> 这里需要注意，人群包名称必须和之前创建的人群包名称一致，不可省略。
> id_list是根据cookies抓取的现有账号最新的100条已有人群的ID和人群名称，与填入表格的人群名称进行匹配
- 广告行为
> **`def get_ad_data(cookies,brand_id,cate_id, ad_name, behavior, start_time, end_time, frequency)`**
> 
> ![4](pic/4.png)
> 广告行为目前只支持品牌维度、品牌x三级类目，三级类目维度使用场景较少，没写。
> `渠道`对应用广告行为中的*产品线*,`行为`对应广告行为中的*行为类型*


#### Step3： 无需打开代码程序，只需要配置run.bat文件中的路径，直接运行，但是前提是要有相关的python环境。

![7](pic/7.png)

#### Step4： 生成的表在output文件夹中的output.xlsx中
![3](pic/3.png)


