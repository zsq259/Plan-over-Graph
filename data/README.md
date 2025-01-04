| 名称    | 说明                                              |
| ------- | ------------------------------------------------- |
|         | baseline                                          |
| prompt  | 稍微优化后的精细 prompt 结果                      |
| prompt1 | 改变了输出格式：perform_rule_indx，且模型输出 CoT |
| prompt2 | 改变了输出格式：perform_rule_indx                 |
| prompt3 | 在之前基础上加了输出格式：perform_rule_indx       |
| sft4    | 用自己的代码，改了 compute_loss，3000 组数据训的  |
| sft7    | 用 1000 组数据(?) 没改 compute loss 训了模型后，再用 dpo 训的       |
| sft11   | 用 3000 组数据 没改 compute loss 的 sft             |
|         |                                                   |
|         |                                                   |
|         |                                                   |
|         |                                                   |
|         |                                                   |

