import React, { Component, Alert, useEffect } from 'react';
import './App.css';
import {TextField, Container, FormControl, InputLabel, MenuItem, Select, List} from "@material-ui/core";
import {Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, IconButton, Collapse, Box, Typography} from '@material-ui/core';
import Snackbar from '@material-ui/core/Snackbar';
import {KeyboardArrowUpSharp, KeyboardArrowDownSharp} from '@material-ui/icons/esm';
import { withStyles, makeStyles } from '@material-ui/core/styles';
import API from './utils/API'

import axios from 'axios'
const host = 'http://165.22.177.130:5000'

// reminder includes 1) Loading API 2) Enter but no select 3)
const StyledTableRow = withStyles((theme) => ({
  root: {
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.action.hover,
    },
  },
}))(TableRow);

const StyledTableCell = withStyles((theme) => ({
  head: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  body: {
    fontSize: 14,
    height: 15,
  },
}))(TableCell);

function Headhide(props){
  const dohide = props.dohide;

  if (!dohide){
    return(
        <TableHead>
          <StyledTableRow>
            <StyledTableCell>DETAIL</StyledTableCell>
            <StyledTableCell>CONTENT</StyledTableCell>
          </StyledTableRow>
        </TableHead>
    )
  }
  return (<TableHead/>);
}

function Thead(props){
  const dohide = props.dohide;
  const [open, setOpen] = React.useState(false);
  const d = props.result;
  // const [detail, setDet] = React.useState({});
  const [detail, setDet] = React.useState({});

  useEffect(()=>{
    getDetail();
  }, []);
  // setDet(response.data);

  const getDetail = async ()=> {
    const response = await axios.get(host+`/detail?code=${d.code}&&limit=10`);
    setDet(response.data);
  }

  if (!dohide){
    return(
        <React.Fragment>
          <TableRow key={d}>
            <TableCell>
              <IconButton aria-label="expand row" size="small" onClick={() => setOpen(!open)}>
                {open ? <KeyboardArrowUpSharp /> : <KeyboardArrowDownSharp />}
              </IconButton>
            </TableCell>
            <TableCell>{d.display}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
              <Collapse in={open} timeout="auto" unmountOnExit>
                <Box margin={1}>
                  <Typography variant="h6" gutterBottom component="div">
                    {/* Details */}
                  </Typography>
                  <Table size="small">
                    <TableHead>
                      <StyledTableRow>
                        <StyledTableCell>Title</StyledTableCell>
                        <StyledTableCell>Genre</StyledTableCell>
                        <StyledTableCell>Act</StyledTableCell>
                        <StyledTableCell>Scene</StyledTableCell>
                        <StyledTableCell>Line(s)</StyledTableCell>
                        <StyledTableCell>Speaker</StyledTableCell>
                      </StyledTableRow>
                    </TableHead>
                    <TableBody>
                      <TableRow>
                        <TableCell className="DispTable">{detail.title}</TableCell>
                        <TableCell>{detail.genre}</TableCell>
                        <TableCell>{d.actnum}</TableCell>
                        <TableCell>{d.scnum}</TableCell>
                        <TableCell>{d.lineRange}</TableCell>
                        <TableCell>{d.speaker}</TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                  <Table>
                    <TableHead>
                      <StyledTableRow>
                        <StyledTableCell>Photo</StyledTableCell>
                        <StyledTableCell>Synopsis</StyledTableCell>
                      </StyledTableRow>
                    </TableHead>
                    <TableBody>
                      <TableRow>
                        <TableCell >
                          <img src ={require('./covers/' + d.code.toString() + '.jpg').default}
                               className="detail-img"/>
                        </TableCell>
                        <TableCell>{detail.synopsis}</TableCell>
                      </TableRow>
                      <TableRow>
                        {/* {
                          detail.otherlines.map((item, i) => {
                            return <TableCell key={i}>{item.display}</TableCell>
                          })
                        } */}
                      </TableRow>
                    </TableBody>
                  </Table>
                </Box>
              </Collapse>
            </TableCell>
          </TableRow>
        </React.Fragment>
    )
  }
  return null;
}

function Wordslist(props){
  const words = props.words;

  if (words){
    return (
        <div>
          {
            <ul>
              {words.map(function(d, idx){
                return (<li key={idx}>{d}</li>)
              })}
            </ul>
          }
        </div>
    )
  }
  return null;
}

function SugWordslist(props){
  const sugwords = props.sugwords;

  if (sugwords){
    return (
        <div>
          {
            <ul>
              {sugwords.map(function(d, idx){
                return (<li key={idx}>{d}</li>)
              })}
            </ul>
          }
        </div>
    )
  }
  return null;
}

export default class App extends Component {

  constructor(props){
    super(props)
    this.state={
      Mouseopen: '',
      type: '',
      open: false,
      query: '',
      suggestions: [],
      check: {}, // only for tesing
      results: [],
      words: [],
      sugWords:[],
      sugTotal:0,
      dohide: true,
    }
    this.MouseOver = this.MouseOver.bind(this);
    this.MouseOver = this.MouseOver.bind(this);
  }

  handleChange = (event) => {
    this.setState({type: event.target.value})
    console.log(this.state.type)
  };
  handleClose = () => {
    this.open = false;
  };
  handleOpen = () => {
    this.open = true;
  };

  onSearchchange = e => {
    const query = e.target.value;
    this.setState({dohide: true});
    if (!query){
      this.setState({suggestions: []});
    } else if (query.length) {
      this.setState({ query: query }, async () => {
        this.querySuggestion(query);
      })
      if (this.state.type === 40) {
        this.Searchpho(query);
        this.setState({sugWords: []});
      } else if (this.state.type === 30){
        this.RegularEx(query);
        this.setState({words: []});
      } else {
        this.setState({words: [], sugWords: []})
      }
    }
  };

  querySuggestion = async query => {
    const response = await axios.get(host+`/searchtext?text==${query}`);
    const arr = []
    Object.keys(response.data).forEach(key => arr.push({name: key, value: response.data[key].substring(1)}))
    this.setState({ suggestions: arr})
    // this.setState({ suggestions: response.data})
  };

  toEnter = e => {
    const query = e.target.value;
    this.setState({dohide: true});
    this.setState({regalert:false, showalert: false, resultalert:false})
    if (e.key === "Enter") {
      if (query.length) {
        // also set query type
        // add ...
        this.setState({ query, words:[], sugWords:[], results: [], suggestions: [] }, async () => {
          this.querySearch(query);
        })
      } else {
        this.setState({resultalert: true, warningTitle: "Invalid", warning: "Query shall not be empty.", severity: "warning"})
      }
    }
  };

  querySearch = async query => {
    // call different query functions
    // add ...
    if(this.state.type===10)
      this.BM25Oa(query);
    if(this.state.type===20)
      this.BM25Or(query);
    if(this.state.type===30)
      this.RegularEx(query);
    if(this.state.type===40)
      this.Searchpho(query);
  }

  BM25Oa = async query => {
    this.setState({ check: "inor", suggestions:[]});
    // add loading
    this.setState({showalert: true})
    const response = await axios.get(host+`/querybm25?query==${query}&&andor=0&&limit=100000`);
    console.log(response.data.result.length)
    this.setState({showalert: false});
    if(response.data.result.length>0){
      this.setState({ results: response.data.result, dohide: false, showalert: false});
    }
    else {
      this.setState({resultalert: true});
    }

  }

  BM25Or = async query => {
    this.setState({ check: "inor", suggestions:[]});
    // add loading
    this.setState({showalert: true})
    const response = await axios.get(host+`/querybm25?query==${query}&&andor=1&&limit=100000`);
    this.setState({showalert: false});
    this.setState({showalert: false});
    console.log(response.data)
    if(response.data){
      this.setState({ results: response.data.result, dohide: false, showalert: false});
    }
    else {
      this.setState({resultalert: true});
    }
  }

  RegularEx = async query => {
    const response = await axios.get(host+`/querysug?query=${query}`);
    console.log(response.data.result)
    this.setState({regalert:false, showalert: false});
    if(response.data.result.length>=10){
      this.setState({regalert:true,sugWords:response.data.result,suggestions:[], dohide: true,sugTotal:response.data.result.length});
    }
    else if(response.data.result.length>0) {
      this.setState({showalert: true});
      const responsereg = await axios.get(host+`/queryreg?query=${query}&&limit=1000`);
      console.log(responsereg.data.result) //我把这个放到了bm25的results里面
      this.setState({results:responsereg.data.result, dohide: false, suggestions: [], showalert: false});
    }
    else if(response.data.result.length=0){
      this.setState({resultalert: true});
    }
  }

  Searchpho =  async query =>{
    const response = await axios.get(host+`/searchpho?word=${query}`);
    this.setState({showalert: false});
    console.log(response.data)
    if (response.data){
      this.setState({words: response.data.result, dohide: true, showalert: false});
      // if (response.data.result.length<10){
      //   const newquery = this.state.words.join(' ');
      //   const responsepho = await axios.get(host+`/querybm25?query==${newquery}&&andor=1&&limit=100`);
      //   console.log(responsepho.data.result) //我把这个放到了bm25的results里面
      //   this.setState({results: responsepho.data.result, dohide: false, suggestions: [], showalert: false});
      // }
    } else {
      this.setState({resultalert: true});
      this.setState({words:[],suggestions:[], dohide: true, showalert: true});
    }
  }

  MouseOver(e){
    this.state({
      MouseOpen: 'hover',
    })
  }

  MouseOut(e){
    this.state({
      MouseOpen: '',
    })
  }

  render() {
    const {suggestions} = this.state
    return (
        <div className="App">
          <div className="Cover"></div>
          <header className="App-header">
            <Container>
              <label style={{fontSize: '70px'}}>Shakespeare Search</label>
              <div className="SearchBlock">
                <FormControl>
                  <InputLabel style={{
                    fontFamily: 'Courier New',
                    fontSize: '20px',
                  }} >type</InputLabel>
                  <Select
                      onChange = {this.handleChange}
                      defaultValue = {50}
                      className="Select"
                  >
                    <MenuItem className="Menuitem" value={50}><em>DoSelect</em></MenuItem>
                    <MenuItem className="Menuitem" value={10}>BM25And</MenuItem>
                    <MenuItem className="Menuitem" value={20}>BM25Or</MenuItem>
                    <MenuItem className="Menuitem" value={30}>RegularEx</MenuItem>
                    <MenuItem className="Menuitem" value={40}>Phonetics</MenuItem>
                  </Select>
                </FormControl>
                <TextField className="Query" variant="standard" placeholder="Please choose type and enter your query ~"
                           options={suggestions.map((option) => option.value)}
                           onChange={this.onSearchchange} onKeyPress={this.toEnter}
                />
                <Snackbar
                    anchorOrigin={{
                      vertical: 'bottom',
                      horizontal: 'left',
                    }}
                    open={this.state.showalert}
                    autoHideDuration={6000}
                    message="Please wait patiently."
                />
                <Snackbar
                    anchorOrigin={{
                      vertical: 'top',
                      horizontal: 'middle',
                    }}
                    open={this.state.resultalert}
                    autoHideDuration={6000}
                    message="This is no result"
                />
                <Snackbar
                    anchorOrigin={{
                      vertical: 'top',
                      horizontal: 'middle',
                    }}
                    open={this.state.regalert}
                    autoHideDuration={6000}
                    message={"There are a total of "+ this.state.sugTotal.toString()+
                    " words that match your input, Regular search is not recommended. Any following words you need?"}
                />
              </div>
            </Container>
            <div className="DisplayAll">
              <Paper elevation={0} style={{maxHeight: 400, width: 150, backgroundColor: 'rgba(52, 52, 52, 0.0)', overflow: 'auto'}}>
                <List>
                  <div className='LeftList'>
                    <div>
                      <Wordslist words={this.state.words}/>
                    </div>
                    <div>
                      <SugWordslist sugwords={this.state.sugWords}/>
                    </div>
                  </div>
                </List>
              </Paper>
              <div className="RightPart">
                <Container className="Suggestion">
                  <ul>
                    {Object.keys(suggestions).map(function(Index,name){
                      return (
                          <li key={Index}>
                            {suggestions[Index].value}
                          </li>
                      )
                    })}
                  </ul>
                </Container>
                <Paper elevation={5} className={this.state.dohide?"HideP":"ShowP"} style={{maxHeight: 500, width: 700, backgroundColor: 'rgba(52, 52, 52, 0.0)', overflow: 'auto'}}>
                  <div className="TableResult">
                    <TableContainer class = "hidden" component={Paper}>
                      <Table stickyHeader>
                        <Headhide dohide={this.state.dohide} />
                        <TableBody>
                          {this.state.results.map((d) =>(
                              <Thead result={d} dohide={this.state.dohide} />
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </div>
                </Paper>
              </div>
            </div>
          </header>
        </div>
    );
  }
}