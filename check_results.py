import os


def check_results():
  count = 0
  growth = 0
  file  = open('results.txt', 'r')
  results = file.read()
  for week in results:
    line = week.split()
    if count >= 9700:
      continue
    else:
      count += 1
      if float(line[3]) > float(line[0]):
        growth += 1
  file.close()
  print('final ratio: ' + str(float(growth) / float(count)))
  
  
if __name__ == '__main__':
  check_results()
