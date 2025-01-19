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
| sft12   | 用 10-3-1000 直接训                                |
| sft13   |    10-30-3-2000 接着 12 的训                       |
| sft14   |    3000 组接着 13 的训                             |
| sft15   |    17 上面训的直接 3000组                          |
| sft16   |    17 上面混合 alpaca_gpt4 訓的                    |

